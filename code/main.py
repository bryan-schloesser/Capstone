# Importing Libraries for use

import numpy
import pandas
import plotly.express as plotly
from flask import request, Flask
from jsonify.convert import jsonify

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

import tensorflow
import flask

import matplotlib as plot
import seaborn


app = Flask(__name__)


@app.route('/pass_val', methods=['POST'])
def pass_val():
    name = request.args.get('value')
    print('name', name)
    return jsonify({'reply': 'success'})


# Imports data for both white and red wine as seperate data
# white_wine_data = pandas.read_csv("./data/winequality-white.csv", delimiter=';')
red_wine_data = pandas.read_csv("./data/winequality-red.csv", delimiter=';')

# print(white_wine_data.head())
print(red_wine_data.head())

# Find correlation between quality and the chemical values
# white_wine_corr = white_wine_data.corr()['quality'].drop('quality')
red_wine_corr = red_wine_data.corr()['quality'].drop('quality')


# Function to return correlations higher than a user defined threshold
def high_corr(wine_type_corr, threshold):
    av_correlations = wine_type_corr.abs()
    high_correlations = av_correlations[av_correlations > threshold].index.values.tolist()
    return high_correlations


# Taking chemicals with high correlation as the x input and taking quality as the y input
chems = high_corr(red_wine_corr, 0.05)
print(chems)
x = red_wine_data[chems]
y = red_wine_data['quality']

# Creation of both test and production data sets
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=3)

# Linear Regression model
reg = LinearRegression()
reg.fit(x_train, y_train)

print(reg.coef_)

# Predict Quality
train_pred = reg.predict(x_train)
print(train_pred)
test_pred = reg.predict(x_test)
print(test_pred)

# calculating RMSE
train_rmse = metrics.mean_squared_error(train_pred, y_train) ** 0.05
print(train_rmse)
test_rmse = metrics.mean_squared_error(test_pred, y_test) ** 0.05
print(test_rmse)

# rounding off the predicted values for the test set
predicted_data = numpy.round_(test_rmse)
print(predicted_data)

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, test_pred))
print('Mean Squared Error: ', metrics.mean_squared_error(y_test, test_pred))
print('Root Mean Squared Error: ', numpy.sqrt(metrics.mean_squared_error(y_test, test_pred)))

# displaying coefficients of each chemical

coefficients = pandas.DataFrame(reg.coef_, chems)
coefficients.columns = ['Coefficients']
print(coefficients)

# This is to pull custom chemical values to determine quality for any wine.
val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11 = 7.4, .7, 0, 1.9, .076, 11, \
                                                                     34, 0.9978, 3.51, .56, 9.4
d = {'fixed acidity': val1, 'volatile acidity': val2, 'citric acid': val3, 'residual sugar': val4, 'chlorides': val5,
     'free sulfur dioxide': val6, 'total sulfur dioxide': val7, 'density': val8, 'pH': val9, 'sulphates': val10,
     'alcohol': val11}
user_wine = pandas.DataFrame(data=d, index=[0])
wine_to_rate = user_wine[chems]

# Prediction test
predict_wine_quality = reg.predict(wine_to_rate)
print("Wine Quality Prediction: ")
print(predict_wine_quality)
