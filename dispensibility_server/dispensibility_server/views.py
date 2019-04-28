from dispensibility_server import app, db
from dispensibility_server.models import *
from flask import render_template, url_for, abort, request, redirect
import json

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/myitems")
def myitems():
    return render_template("myitems.html")

@app.route("/purchase")
def purchase():
    return render_template("purchase.html")

@app.route("/additem")
def additem():
    return render_template("additem.html")
    
@app.route('/api/dispense_transaction', methods=['POST'])
def dispense_transaction(input):
    input_json = json.loads(input)
    dispenser_id = input_json.get('dispenser_id',None)
    user_id = input_json.get('user_id',None)
    event = input_json.get('event',None)
    weight = input_json.get('weight',None)
    timestamp = input_json.get('timestamp',None)

    assert type(dispenser_id).__name__ == 'int', "Dispenser_id not integer or is None"
    assert type(user_id).__name__ == 'int', "User_id not integer or is None"
    assert type(event).__name__ == 'str', "Event not integer or is None"
    assert type(timestamp).__name__ == 'str', "Timestamp not integer or is None"
    assert type(timestamp).__name__ == 'str', "Timestamp not integer or is None"

    # TODO: save to db

