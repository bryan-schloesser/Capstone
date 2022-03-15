# Importing Libraries for use
import matplotlib.pyplot
import numpy
import pandas
import plotly
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import plotly.express
import os
import seaborn


# Function used to return the names of the chemicals that have a correlation threshold of a modifiable value.
# The function takes inputs of both wine correlation data and threshold to make the method more versatile.
def high_corr(wine_type_corr, threshold):
    # converts all correlations to positive float values in order to easily determine which chemicals have the most
    # impact on quality regardless of whether that be positive or negative.
    av_correlations = wine_type_corr.abs()
    # adds the names of the chemical that have high correlation to a list
    high_correlations = av_correlations[av_correlations > threshold].index.values.tolist()
    return high_correlations


# Imports the wine data from the csv file and creates a dataframe from it.
red_wine_data = pandas.read_csv("./data/winequality-red.csv", delimiter=';')

# Creates a seperate dataframe of the correlation the chemicals have on quality
red_wine_corr = red_wine_data.corr()['quality'].drop('quality')

# Taking chemicals with high correlation as the x input and taking quality as the y input.
chems = high_corr(red_wine_corr, 0.05)
x = red_wine_data[chems]
y = red_wine_data['quality']

# Creation of both test and train data sets.
xtrain, xtest, ytrain, ytest = train_test_split(x, y, random_state=3)

# Linear Regression model.
reg = LinearRegression()
reg.fit(xtrain, ytrain)

# Predict Quality for both train and test data sets.
train_pred = reg.predict(xtrain)
test_pred = reg.predict(xtest)

# calculating RMSE.
prod_rmse = metrics.mean_squared_error(train_pred, ytrain) ** 0.05
test_rmse = metrics.mean_squared_error(test_pred, ytest) ** 0.05

# Displaying coefficients of each chemical.
coefficients = pandas.DataFrame(reg.coef_, chems)
coefficients.columns = ['Coefficients']


# Function that will make a bar graph out of the red wine data to display the total amounts of wine that are of each
# quality rating.
def graph1():
    # dict of the quality values and the total numbers of wine for each quality rating
    d = {"quality": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "total": []}

    # Loops through the quality values and uses those to determine which wines to count from the wine data.
    # Time complexity of O(n) where the n is the amount of wines.
    for i in range(1, 11):
        wine_count = 0  # Keeps track of how many wines are of the quality it is currently focused on.
        # For each wine in the list of wine data, add the wine to the wine counter if the quality rating matches
        # the quality rating it is currently getting a tally for.
        for wine in range(1, len(red_wine_data["quality"].values)):
            if i == red_wine_data["quality"].values.tolist()[wine]:
                wine_count += 1
        d["total"].append(wine_count)  # append count to the d dict.

    df = pandas.DataFrame(data=d)  # Creates a dataframe of the data once all quality ratings have been tallied.

    # Creates a bar graph based on the quality amounts and the totals
    bar = plotly.express.bar(df, x='quality', y='total', template="ggplot2")
    # If the images path does not exist, create it, so we have a place to keep the image of the graph.
    if not os.path.exists("images"):
        os.mkdir("images")
    bar.write_image("images/graph1.png")  # Create image of the graph
    return 'images/graph1.png'  # returns file path of image to know what image to render in web page.


# Function that creates a scatter plot graph based on the correlation alcohol has to the quality of the wine.
def graph2():
    # Uses the wine data and creates a scatter plot based on alcohol and quality values.
    scatter_plot = plotly.express.scatter(red_wine_data, x="alcohol", y="quality", template="ggplot2")

    # If the images path does not exist, create, so we have a place to keep the image of the graph.
    if not os.path.exists("images"):
        os.mkdir("images")
    scatter_plot.write_image("images/graph2.png")  # Create image of the graph
    return 'images/graph2.png'  # returns file path of image to know what image to render in web page.


# Function that creates a heatmap of the correlation data to determine what chemicals have what correlation to quality.
def graph3():
    matplotlib.pyplot.figure(figsize=(40.0, 38.0))  # Sets size of graph
    seaborn.set_theme(font_scale=4)  # Sets the font size of the labels in the graph
    seaborn.heatmap(red_wine_data.corr())  # Creates heatmap based on the correlation data.
    # If the images path does not exist, create, so we have a place to keep the image of the graph.
    if not os.path.exists("images"):
        os.mkdir("images")
    matplotlib.pyplot.savefig('images/graph3.png')  # Create image of the graph
    return 'images/graph3.png'  # returns file path of the image to know what image to render in web page.


# This method is used to get the prediction of any wine the users enter.
def get_prediction(chem_list):
    # Creates a dict based on the data the user entered via the front-end.
    d = {'fixed acidity': chem_list[0], 'volatile acidity': chem_list[1], 'citric acid': chem_list[2],
         'residual sugar': chem_list[3],
         'chlorides': chem_list[4],
         'free sulfur dioxide': chem_list[5], 'total sulfur dioxide': chem_list[6], 'density': chem_list[7],
         'pH': chem_list[8], 'sulphates': chem_list[9],
         'alcohol': chem_list[10]}
    # Creates a dataframe from the dict
    user_wine = pandas.DataFrame(data=d, index=[0])
    # Uses the correlation values from the high_corr method and only keeps the chemical values that are above x
    # threshold.
    wine_to_rate = user_wine[chems]

    # Predicts the quality of the wine using linear regression based on the values of the wine the user entered.
    predict_wine_quality = int(reg.predict(wine_to_rate))

    # Returns a string value of the wine quality to present to the user on the web page.
    return str(predict_wine_quality)
