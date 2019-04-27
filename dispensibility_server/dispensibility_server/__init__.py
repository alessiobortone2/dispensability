from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config') # load default
app.config.from_pyfile('config.py') #load instance/config.py
db = SQLAlchemy(app)

from dispensibility_server.models import * 

#init the database if it doesn't exist
db.create_all()
db.session.commit()

from dispensibility_server import views
