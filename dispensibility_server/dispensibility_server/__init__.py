from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config') # load default
app.config.from_pyfile('config.py') #load instance/config.py
db = SQLAlchemy(app)

from dispensibility_server.models import * 
exists = os.path.isfile('{}/dispensibility.db'.format(os.getcwd()))

if not exists:
  #init the database if it doesn't exist
  print("creating db")
  db.create_all()

  # Create mock user
  user = User(login = 'illy',
              password = 'pass',
              first_name = 'Ilian',
              last_name = 'Mitev',
              postcode = 'CB4 1PZ',
              created_on = datetime.now())

  oats = Product(name = 'Oats',
                    allergens = 'May contain oats.',
                    description = 'Delicious and nutrituous oats! Also healthy!',
                    density = 2.51,
                    price_per_gram = 0.0059)

  db.session.add_all([user,
                      oats])

  db.session.commit()

  dispenser = Dispenser(product_id = oats.id)
  db.session.add(dispenser)
  db.session.commit()

from dispensibility_server import views
