from dispensibility_server import app, db
from sqlalchemy import Integer, String, DateTime, Float, ForeignKey

class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column('uid' , Integer, primary_key=True)
    login = db.Column('login' , String(255))
    password = db.Column('password', String(100))
    first_name = db.Column('first_name', String(100))
    last_name = db.Column('last_name', String(100))
    postcode = db.Column('postcode', String(100))
    created_on = db.Column('created_on', DateTime())

class Dispenser(db.Model):
  __tablename__ = 'dispenser'
  id = db.Column('id', Integer, primary_key=True)
  product_id = db.Column('product_id', ForeignKey("product.id"), nullable=False)

class Product(db.Model):
  __tablename__ = 'product'
  id = db.Column('id', Integer, primary_key=True)
  allergens = db.Column('allergens', String(1000))
  description = db.Column('description', String(1000))
  density = db.Column('density',Float())
  price_per_gram = db.Column('price_per_gram',Float())

class Refill(db.Model):
  __tablename__ = 'refill'
  id = db.Column('id', Integer, primary_key=True)
  dispenser_id = db.Column('dispenser_id', ForeignKey("dispenser.id"), nullable=False)
  product_id = db.Column('product_id', ForeignKey("product.id"), nullable=False)
  timestamp = db.Column('timestamp', DateTime())

class DispenserTransactionEvent(db.Model):
  __tablename__ = 'dispenser_transaction_event'
  id = db.Column('id', Integer, primary_key=True)
  user_id = db.Column('user_id', ForeignKey("user.uid"), nullable=False)
  dispenser_id = db.Column('dispenser_id', ForeignKey("dispenser.id"), nullable=False)
  event = db.Column('event', String())
  weight = db.Column('weight', Integer())
  timestamp = db.Column('timestamp', DateTime())

class UserTransaction(db.Model):
  __tablename__ = 'user_transaction'
  id = db.Column('id', Integer, primary_key=True)
  user_id = db.Column('user_id', ForeignKey("user.uid"), nullable=False)
  dispenser_id = db.Column('dispenser_id', ForeignKey("dispenser.id"), nullable=False)
  product_id = db.Column('product_id', ForeignKey("product.id"), nullable=False)
  weight = db.Column('weight', Integer())
  cost = db.Column('cost', Float())
  timestamp = db.Column('timestamp', DateTime())
