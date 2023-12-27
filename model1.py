import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib


df = pd.read_csv('priceData/car data.csv')

df['Age'] = 2020 - df['Year']
df['Used_value'] = df['Selling_Price'] / df['Present_Price']
df['Owner'] = df['Owner'] + 1

X = df[['Age', 'Kms_Driven', 'Owner']]
y = df['Used_value']


# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Create linear regression object
regressor = linear_model.LinearRegression()
# Train the model using the training sets
regressor.fit(X_train, y_train)
# Make predictions using the testing set
y_pred = regressor.predict(X_test)
# The coefficients
print("Coefficients: \n", regressor.coef_)
# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))


# # Create an MLPRegressor
# regressor = MLPRegressor(hidden_layer_sizes=(100), max_iter=1000, random_state=42)
#
# # Train the model on the training set
# regressor.fit(X_train, y_train)
#
# # Make predictions on the testing set
# y_pred = regressor.predict(X_test)
#
# # Calculate Mean Absolute Error (MAE)
# mae = mean_absolute_error(y_test, y_pred)
# print(f'Mean Absolute Error (MAE): {mae}')
#
# # Calculate Root Mean Squared Error (RMSE)
# rmse = mean_squared_error(y_test, y_pred, squared=False)
# print(f'Root Mean Squared Error (RMSE): {rmse}')

# Save the model to a file
joblib.dump(regressor, 'mlp_regressor_model.joblib')



