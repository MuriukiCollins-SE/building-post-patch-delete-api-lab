#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if request.method == 'GET':
        bakery_serialized = bakery.to_dict()
        return make_response(bakery_serialized, 200)
    elif request.method == 'PATCH':
        data = request.form
        if 'name' in data:
            bakery.name = data['name']
            db.session.commit()
        return make_response(bakery.to_dict(), 200)

@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'GET':
        baked_goods = [bg.to_dict() for bg in BakedGood.query.all()]
        return make_response(baked_goods, 200)
    elif request.method == 'POST':
        data = request.form
        new_bg = BakedGood(
            name=data.get('name'),
            price=data.get('price'),
            bakery_id=data.get('bakery_id')
        )
        db.session.add(new_bg)
        db.session.commit()
        return make_response(new_bg.to_dict(), 201)

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter_by(id=id).first()
    if baked_good:
        db.session.delete(baked_good)
        db.session.commit()
        return make_response({'message': 'Baked good deleted successfully'}, 200)
    else:
        return make_response({'error': 'Baked good not found'}, 404)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)