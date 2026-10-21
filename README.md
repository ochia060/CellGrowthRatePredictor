# Cell Growth Rate Prediction
This program predicts cell growth rate based on temperature, pH, [glucose], and [lactate] using polynomial regression
and KNN regression.\
The models are trained and tuned on a dataset, and a "best model" is chosen based on the rmse value obtained.

## Highlights

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
Two models were chosen to predict cell growth rate:
- polynomial regression
- KNN regression
A pipeline is run which standardizes the data and fits it to the chosen model, which includes linear regression for 
the polynomial regression model.
A grid is then created testing different parameters for each model in order to find the best fitting one. For polynomial
regression, multiple degrees were tested, and for KNN regression, the number of neighbours and the weights were tested.

### 3. Model training and tuning
To train and tune the models, a grid search with a four-fold cross validation was used. The hyperparameters (polynomial
degree, number of neighbours, type of weight) were optimised for both models, and the results were saved for later use.

### 4. Model execution and comparison
Each of the tuned models was used on the test data, and the rmse and r2 values were found for each.\
The results of each model for predicting cell growth rate were compiled in a table for easy comparison. This table is 
printed in the terminal, and also exported as a .csv file after main.py execution.\
The final model chosen was the one which demonstrated the smallest rmse value.

### 5. Graphical comparison and validation
Validation curves were generated for each model, showing the ideal hyperparameters to fit the data.\
A graph comparing the cell growth rate calculated by the final chosen model and the actual data was also created.

## Analysis

### Model Architecture

### Model Comparison

### Model Advantages and Limitations

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



### Model Applications



        
        Highlights
            Heading 2
            3 - 10 words per bullet point
            Include 5 bullet points in an unordered list.
            Begin each bullet point with an action verb.
                E.g., https://capd.mit.edu/resources/resume-action-verbs/
            Focus on significant technical work, such as what you built, designed, implemented, optimized, tested, or learned.
            Consider what you would want a potential employer to know about your Python skills after reading this section.
        Code Design
            Heading 2
            500 - 1000 words
            Describe the workflow of the program after main.py is executed.
            Explain the purpose of each major stage of the workflow and why it exists.
            Examples of major stages include (but are not limited to) data loading, preprocessing, feature engineering, model training, etc.
            Do not simply list the functions and classes that are called.
            Organize this section using Heading 3 subsections.
            For each subsection, describe:
                What does this stage of the workflow do?
                Why is this stage necessary?
                How does this stage contribute to the overall workflow?
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

    Additional Information:
        There is not a single correct model architecture.
        You are primarily being evaluated on your ability to justify your choice of model architecture rather than developing a model with the lowest possible error.
        Figures and tables do not count towards the word count.
        Word limits should be viewed as strong suggestions, rather than hard limits.
        You can use this website to convert CSV to Markdown, if needed: https://convertcsv.com/csv-to-markdown.htm
        You should present your repository like a portfolio project rather than an assignment for a course. I would encourage you not to make any references to the course (e.g., course code, course name, assignment number, student ID, etc.).
        You can find a guide to the major Markdown syntax elements here: https://www.markdownguide.org/cheat-sheet/
