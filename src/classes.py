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

        #  make the regression models.
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

    def train_and_compare(self):
        # cross-validation on training data to compare models
        comparison = []
        tuned_models = {}

        for name, model in self.models.items():
            grid_search = GridSearchCV(
                estimator=model,
                param_grid=self.param_grids[name],
                cv=5,
                scoring={
                    "RMSE": "neg_root_mean_squared_error",
                    "R2": "r2"
                },
                refit="RMSE",
                n_jobs=-1
            )

            grid_search.fit(self.x_train, self.y_train)

            # return best model from grid search
            best_model = grid_search.best_estimator_
            tuned_models[name] = best_model

            # return cross val. results
            best_index = grid_search.best_index_
            cv_results = grid_search.cv_results_

            mean_cv_rmse = -cv_results[
                "mean_test_RMSE"
            ][best_index]

            mean_cv_r2 = cv_results[
                "mean_test_R2"
            ][best_index]

            cv_r2_std = cv_results[
                "std_test_R2"
            ][best_index]

            # use tuned models on test data
            predictions = best_model.predict(self.x_test)

            test_rmse = root_mean_squared_error(self.y_test, predictions)

            test_r2 = r2_score(self.y_test, predictions)

            comparison.append({
                "Model": name,
                "Best Parameters": str(grid_search.best_params_),
                "Mean CV RMSE": mean_cv_rmse,
                "Mean CV R2": mean_cv_r2,
                "CV R2 Std": cv_r2_std,
                "Test RMSE": test_rmse,
                "Test R2": test_r2
            })

        self.models = tuned_models
        self.results = pd.DataFrame(comparison)

        # return the model with lowest cross val. rmse
        best_index = self.results["Mean CV RMSE"].idxmin()

        self.best_model_name = self.results.loc[
            best_index, "Model"
        ]

        self.best_model = self.models[
            self.best_model_name
        ]

        return self.results


    def export_results(self, filepath):
        if self.results is None:
            raise RuntimeError(
                "Run train_and_compare() first."
            )

        self.results.to_csv(filepath, index=False)

    def export_prediction_plot(self, filepath):
        if self.best_model is None:
            raise RuntimeError(
                "Run train_and_compare() first."
            )

        # Generate predictions using the selected model.
        predictions = self.best_model.predict(self.x_test)

        # Find the range for the perfect-prediction line.
        lower = min(self.y_test.min(), predictions.min())
        upper = max(self.y_test.max(), predictions.max())

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.scatter(
            self.y_test,
            predictions,
            alpha=0.7,
            label="predicted growth rate"
        )

        ax.plot(
            [lower, upper],
            [lower, upper],
            linestyle="-",
            color="black",
            label="perfect prediction"
        )

        ax.set_xlabel("Actual Growth Rate [d^-1]")
        ax.set_ylabel("Predicted Growth Rate [d^-1]")
        ax.set_title(
            f"Actual vs Predicted: {self.best_model_name}"
        )

        ax.legend()

        fig.tight_layout()
        fig.savefig(filepath, dpi=300)
        plt.close(fig)

    def export_comparison_plot(self, filepath):
        # Visualize test-set errors for both models.
        if self.results is None:
            raise RuntimeError(
                "Run train_and_compare() first."
            )

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.bar(
            self.results["Model"],
            self.results["Test RMSE"]
        )

        ax.set_ylabel("Test RMSE [d^-1]")
        ax.set_title("Regression Model Comparison")
        ax.tick_params(axis="x", rotation=15)

        fig.tight_layout()
        fig.savefig(filepath, dpi=300)
        plt.close(fig)

