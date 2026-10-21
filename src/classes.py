import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsRegressor


class CellGrowthCalculator:

    def __init__(self, filepath):
        self.filepath = filepath
        self.data = pd.read_csv(filepath)

        # to set the features (x) and target (y) of the data set
        self.target = "Specific Growth Rate [d^-1]"
        self.features = [
            "Temperature [C]",
            "pH",
            "Glucose [mM]",
            "Lactate [mM]"
        ]

        # to separate the features from the target
        self.x = self.data[self.features]
        self.y = self.data[self.target]

        # to separate the test data from the training data
        self.x_train, self.x_test, self.y_train, self.y_test = (
            train_test_split(
                self.x,
                self.y,
                test_size=0.20,
                random_state=0
            )
        )

        #  to define the models
        self.models = {
            "Polynomial Regression": make_pipeline(
                StandardScaler(),
                PolynomialFeatures(degree=2, include_bias=False),
                LinearRegression()
            ),

            "KNN Regression": make_pipeline(
                StandardScaler(),
                KNeighborsRegressor(n_neighbors=5, weights="uniform"),
            ),
        }

        # hyperparameters to test for each model
        self.param_grids = {
            "Polynomial Regression": {
                "polynomialfeatures__degree": [1, 2, 3, 4]
            },

            "KNN Regression": {
                "kneighborsregressor__n_neighbors": [3, 5, 7, 9, 11],
                "kneighborsregressor__weights": ["uniform", "distance"]
            }
        }

        self.best_model_name = None
        self.best_model = None
        self.results = None
        self.poly_validation_results= None
        self.knn_validation_results = None

    def train_and_compare(self):
        # cross-validation on training data to compare models
        comparison = []
        tuned_models = {}

        for name, model in self.models.items():
            grid_search = GridSearchCV(
                model,
                param_grid=self.param_grids[name],
                cv=4,
                scoring={
                    "RMSE": "neg_root_mean_squared_error",
                    "R2": "r2"
                },
                refit="RMSE",
                return_train_score=True,
                n_jobs=-1
            )

            grid_search.fit(self.x_train, self.y_train)

            # save results for the polynomial regression validation curve
            if name == "Polynomial Regression":
                cv_results = grid_search.cv_results_

                self.poly_validation_results = pd.DataFrame({
                    "Polynomial Degree": cv_results[
                        "param_polynomialfeatures__degree"
                    ].astype(int),
                    "Train RMSE": -cv_results["mean_train_RMSE"],
                    "Valid RMSE": -cv_results["mean_test_RMSE"]
                })

                self.poly_validation_results = (
                    self.poly_validation_results.sort_values("Polynomial Degree")
                    .reset_index(drop=True)
                )

            # save results for the KNN validation curve
            if name == "KNN Regression":
                cv_results = grid_search.cv_results_

                self.knn_validation_results = pd.DataFrame({
                    "Neighbours": cv_results[
                        "param_kneighborsregressor__n_neighbors"
                    ].astype(int),
                    "Weights": cv_results[
                        "param_kneighborsregressor__weights"
                    ].astype(str),
                    "Train RMSE": -cv_results["mean_train_RMSE"],
                    "Valid RMSE": -cv_results["mean_test_RMSE"]
                })

                self.knn_validation_results = (
                    self.knn_validation_results
                    .sort_values(["Weights", "Neighbours"])
                    .reset_index(drop=True)
                )

            # return best model from grid search
            best_model = grid_search.best_estimator_
            tuned_models[name] = best_model

            # return cross val. results
            best_index = grid_search.best_index_
            cv_results = grid_search.cv_results_

            mean_cv_rmse = -cv_results["mean_test_RMSE"][best_index]

            mean_cv_r2 = cv_results["mean_test_R2"][best_index]

            cv_r2_std = cv_results["std_test_R2"][best_index]

            # use tuned models on test data
            predictions = best_model.predict(self.x_test)

            # find rmse where smaller value = less error
            test_rmse = root_mean_squared_error(self.y_test, predictions)

            # find r2 where value closer to 1 = less error
            test_r2 = r2_score(self.y_test, predictions)

            # to format things nicer
            if name == "KNN Regression":
                best_parameters = (
                    f"Neighbours = "
                    f"{grid_search.best_params_['kneighborsregressor__n_neighbors']}, "
                    f"Weights = "
                    f"{grid_search.best_params_['kneighborsregressor__weights']}"
                )
            else:
                best_parameters = (
                    f"Polynomial Degree = "
                    f"{grid_search.best_params_['polynomialfeatures__degree']}"
                )

            # to compare model parameters via table
            comparison.append({
                "Model": name,
                "Best Parameters": best_parameters,
                "Mean CV RMSE": mean_cv_rmse,
                "Mean CV R2": mean_cv_r2,
                "CV R2 Std": cv_r2_std,
                "Test RMSE": test_rmse,
                "Test R2": test_r2
            })

        self.models = tuned_models
        self.results = pd.DataFrame(comparison)

        # return the result with lowest cross val. rmse
        best_index = self.results["Mean CV RMSE"].idxmin()

        self.best_model_name = self.results.loc[
            best_index, "Model"
        ]

        self.best_model = self.models[
            self.best_model_name
        ]

        # create the table to compare models
        return self.results


    def export_results(self, filepath):

        # to check model training and results
        if self.results is None:
            raise RuntimeError(
                "Run train_and_compare() first."
            )

        self.results.to_csv(filepath, index=False, float_format="%.5f")

    def plot_poly_validation_curve(self, filepath):
        if self.poly_validation_results is None:
            raise RuntimeError(
                "Run train_and_compare() first."
            )

        df = self.poly_validation_results

        degrees = df["Polynomial Degree"].to_numpy()
        rmse_train = df["Train RMSE"].to_numpy()
        rmse_valid = df["Valid RMSE"].to_numpy()

        fig, ax = plt.subplots(
            figsize=(8, 6),
            dpi=400,
            layout="constrained"
        )

        ax.plot(
            degrees,
            rmse_train,
            label="Train (Poly)",
            marker="o",
            linestyle="-",
            color="tab:blue"
        )

        ax.plot(
            degrees,
            rmse_valid,
            label="Validation (Poly)",
            marker="o",
            linestyle="-",
            color="green"
        )

        ax.set_xlabel("Polynomial Degree")
        ax.set_ylabel("Cell Growth Rate RMSE")
        ax.set_title("Polynomial Regression Validation Curve")
        ax.set_xticks(degrees)
        ax.legend()

        fig.savefig(filepath, dpi=400)
        plt.close(fig)

    def plot_knn_validation_curve(self, filepath):
        if self.knn_validation_results is None:
            raise RuntimeError(
                "Run train_and_compare() first."
            )

        df = self.knn_validation_results

        fig, ax = plt.subplots(
            figsize=(8, 6),
            dpi=400,
            layout="constrained"
        )

        # to plot each weighting method
        for weights, linestyle in [
            ("uniform", "-"),
            ("distance", "--")
        ]:
            subset = df[df["Weights"] == weights]

            neighbours = subset["Neighbours"].to_numpy()
            rmse_train = subset["Train RMSE"].to_numpy()
            rmse_valid = subset["Valid RMSE"].to_numpy()

            ax.plot(
                neighbours,
                rmse_train,
                label=f"Train ({weights})",
                marker="o",
                linestyle=linestyle,
                color="tab:blue"
            )

            ax.plot(
                neighbours,
                rmse_valid,
                label=f"Validation ({weights})",
                marker="o",
                linestyle=linestyle,
                color="green"
            )

        ax.set_xlabel("Number of Neighbours")
        ax.set_ylabel("Cell Growth Rate RMSE")
        ax.set_title("KNN Regression Validation Curve")
        ax.set_xticks([3, 5, 7, 9, 11])
        ax.legend()

        fig.savefig(filepath, dpi=400)
        plt.close(fig)

    def export_prediction_plot(self, filepath):
        if self.best_model is None:
            raise RuntimeError(
                "Run train_and_compare() first."
            )

        # predict growth rate on test data with chosen model
        predictions = self.best_model.predict(self.x_test)

        # find min and max values of actual and predicted growth rate
        lower = min(self.y_test.min(), predictions.min())
        upper = max(self.y_test.max(), predictions.max())

        fig, ax = plt.subplots(figsize=(8, 6))

        # for actual vs predicted growth rate data
        ax.scatter(
            self.y_test,
            predictions,
            alpha=0.7,
            color="tab:blue",
            label="model prediction"
        )

        # to make the reference line of a perfectly fitted model
        ax.plot(
            [lower, upper],
            [lower, upper],
            linestyle="-",
            color="black",
            label="perfect prediction"
        )

        ax.set_xlabel("Actual Growth Rate [d^-1]")
        ax.set_ylabel("Predicted Growth Rate [d^-1]")
        ax.set_title(f"Actual vs Predicted Cell Growth Rate: {self.best_model_name}")

        ax.legend()

        fig.tight_layout()
        fig.savefig(filepath, dpi=400)
        plt.close(fig)

    def export_comparison_plot(self, filepath):
        # plot test rmse for both models
        if self.results is None:
            raise RuntimeError(
                "Run train_and_compare() first."
            )

        fig, ax = plt.subplots(figsize=(8, 6))

        bars=ax.bar(
            self.results["Model"],
            self.results["Test RMSE"],
            width=0.4,
            color="tab:blue"
        )

        ax.bar_label(bars, fmt="%.5f", padding=3)

        ax.set_ylabel("Test RMSE [d^-1]")
        ax.set_title("Regression Model Comparison")
        ax.tick_params(axis="x", rotation=10)

        fig.tight_layout()
        fig.savefig(filepath, dpi=400)
        plt.close(fig)

