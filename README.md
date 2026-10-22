# Cell Growth Rate Prediction
This program predicts cell growth rate based on temperature, pH, [glucose], and [lactate] using polynomial regression
and KNN regression.\
The models are trained and tuned on a dataset, and a "best model" is chosen based on the RMSE value obtained.

## Highlights
- Designed a program to predict specific cell growth rate
- Built regression models to fit data
- Optimised model hyperparameters for minimum error
- Tested models on training data using a cross validation grid search
- Created figures and tables summarizing results 

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

### 1. Data loadig and retrieval
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
Each of the tuned models was used on the test data, and the RMSE and R2 values were found for each.\
The results of each model for predicting cell growth rate were compiled in a table for easy comparison. This table is 
printed in the terminal, and also exported as a .csv file after main.py execution.\
The final model chosen was the one which demonstrated the smallest RMSE value.

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
For polynomial regression, polynomial degrees of 1, 2, 3, and 4 were tested. This allowed analysis on whether or not 
a greater model flexibility improved accuracy.
For KNN regression, neighbour counts of 3, 5, 7, 9, and 11 were tested, with uniform and distance-based weighting.


### Model Comparison
The chosen models were compared using root mean squared error (RMSE) and the coefficient of determination (R2).
RMSE measures the magnitude of prediction errors, where a lower value indicates a better prediction by the model.
R2 measures how well the model fits the actual data, where a value closer to 1 indicates a better fit. 
A summary table of results is shown below.

|Model                |Best Parameters                   |Mean CV RMSE|Mean CV R2|CV R2 Std|Test RMSE|Test R2|
|---------------------|----------------------------------|------------|----------|---------|---------|-------|
|Polynomial Regression|Polynomial Degree = 2             |0.15423     |0.28298   |0.01782  |0.15703  |0.38413|
|KNN Regression       |Neighbours = 9, Weights = distance|0.15155     |0.30603   |0.05838  |0.15873  |0.37071|

For this project, the selected "best model" was the one with the lowest cross validation RMSE, which in this case is
KNN regression with 9 neighbours and distance-based weighting.
Looking at the RMSE and R2 values for both models shows only a small difference, indicating that the performance is 
relatively similar.


### Model Advantages and Limitations
Although the model can i

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
For this project, a high specific growth rate is observed when...
and a low specific growth rate is observed when...
The model's ability to predict...

### Model Applications
This model predicts specific cell growth rate based on various factors, and therefore could be applied in the analysis
and planning of experiments involving cell growth.

        Analysis
            Heading 2
            1000 - 2000 words
            Justify your choice of model architecture, including the regression algorithm and hyperparameters.
            Compare your selected model against reasonable alternatives derived from polynomial and k-nearest neighbors regression.
            Provide evidence supporting your conclusions. Evidence may include exported CSV tables, PNG figures, or both.
            Discuss the advantages and limitations of your model.
            Explain how temperature, pH, glucose concentration, and lactate concentration influence specific growth rate.
            Describe cell culture conditions:
                that result in a high specific growth rate.
                that result in a low specific growth rate.
                where the model's predictions may not be reliable.
            Describe potential applications of the model and how it could be used in practice.
            Organize this section using Heading 3 subsections.