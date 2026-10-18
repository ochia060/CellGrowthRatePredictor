
import os

from src.classes import CellGrowthCalculator

filepath_dataset = os.path.join("datasets", "dataset_cell_growth_4factor.csv")

# create the predictor and compare the models
predictor = CellGrowthCalculator(filepath_dataset)

results = predictor.train_and_compare()

# export table for model comparison
predictor.export_results(os.path.join("tables", "model_comparison.csv"))

# export figures
predictor.export_prediction_plot(os.path.join("figures", "predicted_vs_actual.png"))

predictor.export_comparison_plot(os.path.join("figures", "model_comparison.png"))


# summary of results
print("Model comparison:")
print(results.round(4).to_string(index=False))

print("\nSelected model:", predictor.best_model_name)


