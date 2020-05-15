import pandas as pd
import csv
import json
import sys
import main #other pogram

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

@app.route('/')
def output():
    graphs=main.create_graph(main.original_data)
    return render_template('index.html', graphs=graphs,data_lists=main.data_lists)

@app.route('/receiver', methods = ['GET','POST'])
def worker1():   
    symptoms = request.get_json(force=True)
    result = main.prediction(symptoms,0)
    # print(result)
    print("************************************")
    return json.dumps(result)

@app.route('/symptom_nodes', methods = ['GET','POST'])
def worker2():
    symptoms = request.get_json(force=True)   
    result = main.prediction(symptoms,1)
    # print(result)
    print("************************************")
    return json.dumps(result)

@app.route('/diseases_nodes', methods = ['GET','POST'])
def worker3():
    symptoms = request.get_json(force=True)  
    result = main.prediction(symptoms,2)
    # print(result)
    print("************************************")
    return json.dumps(result)


if __name__ == '__main__':
	app.run()