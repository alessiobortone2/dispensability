from flask_sqlalchemy import SQLAlchemy
from dispensibility_server import app, db
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    uid = Column('uid' , Integer, primary_key=True)
    login = Column('login' , String(255))
    password = Column('password', String(100))
    first_name = Column('first_name', String(100))
    last_name = Column('last_name', String(100))
    postcode = Column('postcode', String(100))
    created_on = Column('created_on', DateTime())

class Dispenser(Base):
  __tablename__ = 'dispenser'
  id = Column('id', Integer, primary_key=True)
  product_id = Column('product_id', ForeignKey("product.id"), nullable=False)
  weight = Column('weight', Integer())
  timestamp = Column('timestamp', DateTime())

class Product(Base):
  __tablename__ = 'product'
  id = Column('id', Integer, primary_key=True)
  allergens = Column('allergens', String(1000))
  description = Column('description', String(1000))
  price_per_gram = Column('price_per_gram',Float())

class Refill(Base):
  __tablename__ = 'refill'
  id = Column('id', Integer, primary_key=True)
  dispenser_id = Column('dispenser_id', ForeignKey("dispenser.id"), nullable=False)
  product_id = Column('product_id', ForeignKey("product.id"), nullable=False)
  timestamp = Column('timestamp', DateTime())

class Transaction(Base):
  __tablename__ = 'transaction'
  id = Column('id', Integer, primary_key=True)
  user_id = Column('user_id', ForeignKey("user.uid"), nullable=False)
  dispenser_id = Column('dispenser_id', ForeignKey("dispenser.id"), nullable=False)
  product_id = Column('product_id', ForeignKey("product.id"), nullable=False)
  weight = Column('weight', Integer())
  cost = Column('cost', Float())
  timestamp = Column('timestamp', DateTime())
