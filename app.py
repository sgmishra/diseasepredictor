#!flask/bin/python
import json
import sys

from flask import Flask, render_template, request, redirect, Response
import random, json

app = Flask(__name__)

gra = [{"id": "heavy feeling", "x": -710, "y": 240, "size": 0.5, "color": "#E57821", "label": "heavy feeling"},{"id": "heavy feeling", "x": -710, "y": 240, "size": 0.5, "color": "#E57821", "label": "heavy feeling"},{"id": "heavy feeling", "x": -710, "y": 240, "size": 0.5, "color": "#E57821", "label": "heavy feeling"}]

@app.route('/')
def output():
	# serve index template
	return render_template('index.html', graphs=gra)

@app.route('/receiver', methods = ['GET','POST'])
def worker():
	# read json + reply
    data = request.get_json(force=True)
    result = ''
    print(data)
    print("************************************")

    # for item in data:
    #     result += str(item['make']) + '\n'
    return str(data)

if __name__ == '__main__':
	# run!
	app.run()
# from flask import Flask, jsonify, request, render_template
# app = Flask(__name__)

# @app.route("/hello")
# def hello():
#     return render_template("index.html", name="shubham")

# if __name__ == "__main__":
# 	app.run()