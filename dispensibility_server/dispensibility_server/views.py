from dispensibility_server import app, db
from dispensibility_server.models import *
from flask import render_template, url_for, abort, request, redirect


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/myitems")
def myitems():
    return render_template("myitems.html")
