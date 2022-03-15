import flask
from flask import Flask
from flask import request, render_template, jsonify
from flask_cors import CORS
import main
import json

# Creates an instance of Flask
app = Flask(__name__)
# used to prevent CORS issues while interacting with requests from other sources than itself.
CORS(app)


# Creates an endpoint called get_prediction. Requests coming here will get forwarded over to the get_prediction function
# in the main.py file. it will then return the prediction as a string back to the javascript.
@app.route('/get_prediction', methods=['GET', 'POST'])
def predict():
    # POST request
    myinput = request.form.getlist('listinput[]')  # passes the list of user inputted values for calculation.
    return main.get_prediction(myinput)  # returns the predicted quality as a string value.


# Creates an endpoint called get_graph1. Requests coming here will get forwarded over to the graph1() function in the
# main.py file. It will then return the file path of the image that was generated for the graph.
@app.route('/get_graph1', methods=['GET', 'POST'])
def get_graph1():
    print("I'm working on it!")
    return main.graph1()  # Returns a string of the file path for graph1.


# Creates an endpoint called get_graph1. Requests coming here will get forwarded over to the graph2() function in the
# main.py file. It will then return the file path of the image that was generated for the graph.
@app.route('/get_graph2', methods=['GET', 'POST'])
def get_graph2():
    return main.graph2()


# Creates an endpoint called get_graph1. Requests coming here will get forwarded over to the graph3() function in the
# main.py file. It will then return the file path of the image that was generated for the graph.
@app.route('/get_graph3', methods=['GET', 'POST'])
def get_graph3():
    return main.graph3()

# Runs the web server on the host
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
