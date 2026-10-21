
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

print("Model comparison:")
print(results.round(5).to_string(index=False))

print("\nSelected model:", calculator.best_model_name)