
import os

from src.classes import CellGrowthCalculator

filepath_dataset = os.path.join("datasets", "dataset_cell_growth_4factor.csv")

# create and compare the models
calculator = CellGrowthCalculator(filepath_dataset)

results = calculator.train_and_compare()

# export table for model comparison
calculator.export_results(os.path.join("tables", "model_comparison.csv"))

# export figures for actual vs predicted growth rate and comparison of rmse
calculator.export_prediction_plot(os.path.join("figures", "predicted_vs_actual.png"))

calculator.export_comparison_plot(os.path.join("figures", "model_comparison.png"))

calculator.plot_poly_validation_curve(os.path.join("figures", "poly_validation_curve.png"))

calculator.plot_knn_validation_curve(os.path.join("figures", "knn_validation_curve.png"))

# print a summary table for model comparison
print("Model comparison:")
print(results.round(5).to_string(index=False))

# print the selected model
print("\nSelected model:", calculator.best_model_name)


# to find the largest and smallest growth rate and conditions
df = calculator.data

highest = df.loc[df["Specific Growth Rate [d^-1]"].idxmax()]
lowest = df.loc[df["Specific Growth Rate [d^-1]"].idxmin()]

print("\nConditions for highest observed growth rate:")
print(highest.to_frame().T.to_string(index=False))

print("\nConditions for lowest observed growth rate:")
print(lowest.to_frame().T.to_string(index=False))

# show the conditions that give the 10 largest and smallest growth rate
print("\nLargest growth rate conditions:")
print(
    df.nlargest(5, "Specific Growth Rate [d^-1]")
    .to_string(index=False)
)

print("\nSmallest growth rate conditions:")
print(
    df.nsmallest(5, "Specific Growth Rate [d^-1]")
    .to_string(index=False)
)
