from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mac126218@127.0.0.1:5432/Food'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    price = db.Column(db.Float)

    def __init__(self, id, name, price) :
        self.id = id
        self.name = name
        self.price = price
    
class ProductSchema(ma.Schema) :
    class Meta :
        fields = ('id', 'name','price')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route('/product', methods=['POST'])
def add_product() :
    id = request.json['id']
    name = request.json['name']
    price = request.json['price']

    new_product = Product(id, name, price)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

@app.route('/product', methods=['GET'])
def get_product() :
    all_products = Product.query.all()
    reuslt = products_schema.dump(all_products)
    return jsonify(reuslt)

@app.route('/product/<id>', methods=['GET'])
def get_product_id(id) :
    product = Product.query.get(id)
    return product_schema.jsonify(product)

@app.route('/product/<id>', methods=['PUT'])
def update_product(id) :
    product = Product.query.get(id)

    name = request.json['name']
    price = request.json['price']

    product.name = name
    product.price = price

    db.session.commit()

    return product_schema.jsonify(product)

@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id) :
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)

if __name__ == "__main__" :
    app.debug = True
    app.run(host="127.0.0.2")