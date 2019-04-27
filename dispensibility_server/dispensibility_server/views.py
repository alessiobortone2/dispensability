from dispensibility_server import app, db
from dispensibility_server.models import *
from flask import render_template, url_for, abort, request, redirect
import json

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/sensor_input', methods=['POST'])
def sensor_input(input):
    input_json = json.loads(input)
    weight = input_json.get('weight',None)
    timestamp = input_json.get('timestamp',None)

    assert type(weight).__name__ == 'int', "Weight not integer or is None"
    assert type(timestamp).__name__ == 'str', "Timestamp not integer or is None"

    # TODO: save to db

