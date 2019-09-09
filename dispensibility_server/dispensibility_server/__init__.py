from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

USER_ID = 1
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

  almonds = Product(name = 'Almonds',
                    allergens = 'May contain almonds.',
                    description = 'Delicious and nutrituous oats! Also healthy!',
                    density = 4.51,
                    price_per_gram = 0.008)

  db.session.add_all([user,
                      oats,
                      almonds])

  db.session.commit()

  dispenser_1 = Dispenser(product_id = oats.id)
  dispenser_2 = Dispenser(product_id = almonds.id)
  db.session.add_all([dispenser_1,
                      dispenser_2])
  db.session.commit()

from dispensibility_server import views
