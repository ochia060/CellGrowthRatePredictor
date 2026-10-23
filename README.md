# Cell Growth Rate Prediction
A python based tool that predicts cell growth rate based on temperature, pH, [glucose], and [lactate] using 
polynomial regression and KNN regression.\
The models are trained and tuned on a dataset, and a "best model" is chosen based on the RMSE value obtained.

## Highlights
- Developed a cell growth rate prediction program
- Implemented polynomial and KNN regression pipelines
- Optimized hyperparameters using grid search
- Evaluated models through four-fold cross-validation
- Exported comparison tables and diagnostic figures

## Environment
- Python 3.14.7
- matplotlib 3.11.0
- numpy 2.5.2
- pandas 3.0.5
- sklearn 1.9.0

## Code Design
The major stages when main.py is executed are as follows:
1. data loading and retrieval
2. model building
3. model training and tuning
4. model execution and comparison
5. graphical comparison and validation

### 1. Data loading and retrieval
To start the program, data is loaded and retrieved from the dataset containing the simulated cell growth rate data.
The data is split into the features (Temperature, pH, [Glucose], and [Lactate]) and target (Cell Growth Rate) and then
split into portions for training (80%) and testing (20%) the chosen models.

### 2. Model building
Two models were chosen to predict cell growth rate: polynomial regression and KNN regression.\
A pipeline is run which standardizes the data and fits it to the chosen model, which includes linear regression for 
the polynomial regression model.
A grid is then created testing different parameters for each model in order to find the best fitting one. For polynomial
regression, multiple degrees were tested, and for KNN regression, the number of neighbours and the weights were tested.

### 3. Model training and tuning
To train and tune the models, a grid search with a four-fold cross validation was used. The hyperparameters (polynomial
degree, number of neighbours, type of weight) were optimised for both models, and the results were saved for later use.

### 4. Model execution and comparison
Each of the tuned models was used on the test data, and the RMSE and R² values were found for each.\
The results of each model for predicting cell growth rate were compiled in a table for easy comparison. This table is 
printed in the terminal, and also exported as a .csv file after main.py execution.\
The final model chosen was the one which demonstrated the smallest mean cross validation RMSE value.

### 5. Graphical comparison and validation
Validation curves were generated for each model, showing the ideal hyperparameters to fit the data.\
A graph comparing the cell growth rate calculated by the final chosen model and the actual data was also created.

## Analysis
### Model Architecture
Two regression models, polynomial regression and k-nearest neighbours (KNN) regression were implemented and evaluated to
identify a suitable model for predicting cell growth rate.\
Polynomial regression was chosen due to its capability of representing non-linear relationships between variables while
KNN regression was chosen due to its prediction of target values based on observations with similar input features.\
The model hyperparameters were optimised using grid search with a 4-fold cross validation. The resulting scores give a 
better estimation of model performance in comparison to a standard train-validation split.\
For polynomial regression, polynomial degrees of 1, 2, 3, and 4 were tested. 
For KNN regression, neighbour counts of 3, 5, 7, 9, and 11 were tested, with uniform and distance-based weighting. 
Validation curves were created for each model in order to show the optimal hyperparameter values obtained during tuning.
These curves are shown below.

<img width="3200" height="2400" alt="poly_validation_curve" src="https://github.com/user-attachments/assets/78b3b2e0-3be6-419f-978f-6d3291249588" />

<img width="3200" height="2400" alt="knn_validation_curve" src="https://github.com/user-attachments/assets/35c00fca-2fc6-4ef4-8e8e-08b6e9e8ffba" />


The polynomial validation curve shows that a degree of 2 produces the lowest validation RMSE from the tested degrees. 
Increasing the degree reduces training RMSE, but validation RMSE increases at degrees 3 and 4, suggesting that higher 
degree models fit the training data more closely but risk overfitting the data. Because of this, a degree of 2 was 
selected through hyperparameter optimisation.

The KNN validation curve shows how the number of neighbours and the weighting method affect training and validation 
RMSE. For distance based weighting, the training RMSE is close to zero for all tested neighbour counts, 
while the validation RMSE decreases before reaching the lowest value at 9 neighbours, and then increases slightly. 
This suggests that using nine neighbours with distance based weighting results in the best performance of the tested 
combinations. For uniform weighting, the validation RMSE is also relatively similar for all the tested 
neighbour counts, however it does not achieve a lower error than distance based weighting. As a result, KNN 
regression with 9 neighbours and distance based weighting was selected through grid search.

### Model Comparison
The models were compared using mean cross-validation RMSE, mean cross-validation R², test RMSE, and test R². 
KNN regression with nine neighbours and distance based weighting resulted in the lowest mean cross-validation RMSE of 
0.15155 d⁻¹ and was therefore selected as the final model. Polynomial regression, however, achieved a slightly lower test 
RMSE of 0.15703 d⁻¹ compared with 0.15873 d⁻¹ for KNN, as well as a slightly higher test R² of 0.38413 compared with 0.37071.
A summary table of results is shown below.

|Model                |Best Parameters                   |Mean CV RMSE|Mean CV R²|CV R² Std|Test RMSE|Test R²|
|---------------------|----------------------------------|------------|----------|---------|---------|-------|
|Polynomial Regression|Polynomial Degree = 2             |0.15423     |0.28298   |0.01782  |0.15703  |0.38413|
|KNN Regression       |Neighbours = 9, Weights = distance|0.15155     |0.30603   |0.05838  |0.15873  |0.37071|

These results indicate that the models show a similar performance, with the preferred model depending on the 
evaluation metric (mean CV RMSE). The test R² values suggest that both models explain only part of the variation in 
observed growth rates. As a result, although the selected KNN model performed well according to the cross validation 
selection criteria, its predictions still have uncertainty. 


### Model Advantages and Limitations
An important advantage of this model is that it automates training, hyperparameter optimization, and evaluation.
Using pipelines provides a consistent preprocessing workflow, while grid search systematically compares 
parameter combinations. Each model chosen to test also offers unique advantages to the program.\
Polynomial regression can represent nonlinear relationships and interactions between culture variables, while remaining 
relatively straightforward to fit. One limitation to this is that the behavior depends on the selected polynomial 
degree, and higher-degree models can overfit the data. KNN regression can capture local patterns without requiring a 
single polynomial relationship, however these predictions depend on the distribution of training observations and 
the selected neighbor count and weighting method.\
The main limitation is that both models are trained using a specific dataset and four input variables. Other 
factors (for example cell type) may also influence growth rate are not considered in the current model, therefore 
the predictions based on only the used features may be insufficient to properly predict growth rate.\
Additional datasets or repeated evaluations would help determine whether the model's performance is consistent. 

### Influencing Factors of Cell Growth Rate
Temperature, pH, [glucose], and [lactate] all influence the specific growth rate of cells in a different way.\
Temperature and pH have an optimal range in which cell growth rate is the highest, and 
this range may differ with the type of cell. When temperatures are above the optimal range, there is a risk of denaturing
essential proteins and enzymes, and when temperatures are below the optimal range, cell metabolism slows. Both will result
in a slower growth rate. Conditions above and below the optimal pH range have a similar effect, where cell growth rate slows
due to environmental stress effects.\
Glucose is the primary energy source for many cells, therefore a low concentration can result in less energy production 
and slow growth, and a very high concentration can result in osmotic stress and lactate accumulation.\
Lactate is a typical waste product produced by glycolysis. Excessive concentrations of lactate can lower intracellular pH
and inhibit key metabolic enzymes, reducing growth rate.\
To find the conditions which result in the highest and lowest specif growth rate, 5 observations with the highest and 
5 observations with the lowest growth rate were examined from the data set to identify patterns in temperature, pH,
glucose concentration, and lactate concentration. Both groups showed variability in conditions, suggesting that high 
and low growth rates may not necessarily be explained by a single set of operating conditions. In general, however, it
seems that a higher growth rate is observed with a temperature of ~38 degrees Celsius, a pH of ~7, a glucose concentration 
within the range of 20-33 mM, and a low lactate concentration (0-6 mM). In contrast, a lower growth rate seems to occur
with temperatures of 35-40 C, a pH of 6.4-7.7, lower glucose concentrations (4-18 mM), and higher lactate concentrations
(10-34 mM).\
The 5 highest growth rate observations occurred within a relatively narrow range of conditions, whereas the 5 
lowest growth rate observation (0 d⁻¹) occurred across a wider range of temperatures, pH, glucose 
concentration, and lactate concentration. This suggests that low growth rate may be associated with several different 
combinations of conditions, making the relationship between the input variables and growth rate more 
difficult for the models to learn and predict. As a result of this, predictions at lower growth rates may be less reliable.

### Model Applications
This model predicts specific cell growth rate based on various factors, and therefore could be applied in the analysis
and planning of experiments involving cell growth. For example, researcher's could use this program to estimate cell 
growth rate based on potential conditions, or use it to compare conditions and identify those worth further investigation.
This could help optimise experiments by reducing the number of growth conditions that need to be initially examined.
