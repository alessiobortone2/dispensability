from dispensibility_server import app, db, USER_ID
from dispensibility_server.models import *
from flask import render_template, url_for, abort, request, redirect, jsonify
from datetime import datetime

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/myitems")
def myitems():
    user = db.session.query(User).filter(User.uid==USER_ID).first()
    transactions = db.session.query(UserTransaction).filter(UserTransaction.user_uid==USER_ID).all()
    products = [{'name': db.session.query(Product).filter(Product.id==transaction.product_id).first().name,
                'weight': transaction.weight,
                'cost': transaction.cost} \
            for transaction in transactions]
    print(products)
    return render_template("myitems.html", my_products=products)

@app.route("/purchase")
def purchase():
    return render_template("purchase.html")

@app.route("/additem")
def additem():
    return render_template("additem.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")
    
@app.route('/api/dispense_transaction', methods=['POST'])
def dispense_transaction():
    data = request.get_json()
    dispenser_id = data.get('dispenser_id',None)
    user_id = data.get('user_id',None)
    event = data.get('event',None)
    weight = data.get('weight',None)
    timestamp = data.get('timestamp',None)

    print(data)
    # assert type(dispenser_id).__name__ == 'int', "Dispenser_id ({}) not integer or is None".format(dispenser_id)
    # assert type(user_id).__name__ == 'int', "User_id ({}) not integer or is None".format(user_id)
    # assert type(event).__name__ == 'int', "Event ({}) not integer or is None".format(event)
    # assert type(weight).__name__ == 'int', "Weight ({}) not integer or is None".format(weight)
    # assert type(timestamp).__name__ == 'unicode', "Timestamp ({}) not string or is None".format(timestamp)

    dispenser = db.session.query(Dispenser).filter(Dispenser.id==dispenser_id).first()
    product = db.session.query(Product).filter(Product.id==dispenser.product_id).first()
    user = db.session.query(User).filter(User.uid==user_id).first()

    dt_timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
    dispenser_transaction_event = DispenserTransactionEvent(user_uid = user.uid,
                                                             dispenser_id = dispenser.id,
                                                             event = event,
                                                             weight = weight,
                                                             timestamp = dt_timestamp)

    db.session.add(dispenser_transaction_event)
    db.session.commit()

    if event == 1:
        dispenser_events = db.session.query(DispenserTransactionEvent) \
                            .filter(DispenserTransactionEvent.dispenser_id==dispenser_id) \
                            .filter(DispenserTransactionEvent.user_uid == user.uid) \
                            .order_by(DispenserTransactionEvent.timestamp.desc()).limit(2).all()
        pre_dispense = dispenser_events[1]
        post_dispense = dispenser_events[0]
        weight_delta = pre_dispense.weight - post_dispense.weight
        cost = weight_delta * product.price_per_gram
        print(dispenser_events[1].weight, dispenser_events[0].weight, dispenser_events[1].weight-dispenser_events[0].weight)

        user_transaction_event = UserTransaction(user_uid = user.uid,
                                                 dispenser_id = dispenser_id,
                                                 product_id = product.id,
                                                 weight = weight_delta,
                                                 cost = cost,
                                                 timestamp = datetime.now())

        db.session.add(user_transaction_event)
        db.session.commit()

        return jsonify(user_uid=user_transaction_event.user_uid,
                       dispenser_id=user_transaction_event.dispenser_id,
                       product_id=user_transaction_event.product_id,
                       weight=user_transaction_event.weight,
                       cost=user_transaction_event.cost,
                       timestamp=user_transaction_event.timestamp)

    return jsonify(user_uid=dispenser_transaction_event.user_uid,
                   dispenser_id=dispenser_transaction_event.dispenser_id,
                   event=dispenser_transaction_event.event,
                   weight=dispenser_transaction_event.weight,
                   timestamp=dispenser_transaction_event.timestamp)


@app.route('/api/my_product', methods=['GET'])
def my_product():
  data = request.get_json()
  dispenser_id = data.get('dispenser_id', None)

  dispenser = db.session.query(Dispenser).filter(Dispenser.id == dispenser_id).first()
  product = db.session.query(Product).filter(Product.id == dispenser.product_id).first()

  print(product.to_dict())
  return jsonify(product.to_dict())