import json
import sys
from flask import Flask, jsonify, request
from markupsafe import escape
from mongoengine import *
from bson.objectid import ObjectId

app = Flask(__name__)

DB_NAME = 'test'

connect(DB_NAME)

class Customer(Document):
    name = StringField()
    handphone = StringField()

class Product(Document):
    name = StringField()
    unit_price = FloatField()
    stock_type = IntField()

class Sales(Document):
    customer_id = ReferenceField('Customer')
    product_id = ReferenceField('Product')
    unit_price = FloatField()
    qty = IntField()
    total_price = FloatField()

# CRUD CUSTOMER
# CREATE
@app.route("/customer", methods=['POST'])
def create_customer():
    customer_data = json.loads(request.data)
    try:
        new_customer = Customer()
        if 'name' in customer_data:
            new_customer.name = customer_data['name']
        if 'handphone' in customer_data:
            new_customer.handphone = customer_data['handphone'] 
        new_customer.save()
        return 'Success!', 200
    except Exception as e:
        print('error:', e, file=sys.stderr)
        return 'Failed!', 400

# READ
@app.route("/customer/<id>", methods=['GET'])
def get_customer(id):
    try:
        print('id:', id, file=sys.stderr)
        if (id == '0'):
            print('masuk id 0', file=sys.stderr)
            customers = Customer.objects
        else:
            print('masuk specific id', file=sys.stderr)
            customers = Customer.objects(id=ObjectId(id))
        customer_data = []
        for customer in customers:
            customer_data.append({
                'name': customer.name,
                'handphone': customer.handphone, 
            })
            
        return jsonify(customer_data), 200
    except Exception as e:
        print('error:', e, file=sys.stderr)
        return 'Failed!', 400

# UPDATE
@app.route("/customer/update/<id>", methods=['PUT'])
def update_customer(id):
    try:
        print('id:', id, file=sys.stderr)
        customer = Customer.objects(id=ObjectId(id))
        if customer:
            print('json:', request.json, file=sys.stderr)
            json_data = request.json
            for key in json_data:
                print('key:', key, file=sys.stderr)
                if key == 'name':
                    customer.update_one(set__name=json_data['name'])
                elif key == 'handphone':
                    customer.update_one(set__handphone=json_data['handphone'])

            res = []
            for c in customer:
                res.append({
                    'name': c.name,
                    'handphone': c.handphone,
                })
            return jsonify(res), 200
        else:
            return 'Invalid ID!', 400
    except Exception as e:
        print('error:', e, file=sys.stderr)
        return 'Failed!', 400

# DELETE
@app.route("/customer/delete/<id>", methods=['DELETE'])
def delete_customer(id):
    try:
        print('id:', id, file=sys.stderr)
        customer = Customer.objects(id=ObjectId(id))
        if customer:
            for c in customer:
                c.delete()
            return 'Success delete customer id: ' + id, 200
        else:
            return 'Invalid ID', 400
    except Exception as e:
        print('error:', e, file=sys.stderr)
        return 'Failed!', 400

# CRUD PRODUCT
# CREATE
@app.route("/product", methods=['POST'])
def create_product():
    product_data = json.loads(request.data)
    try:
        new_product = Product()
        if 'name' in product_data:
            new_product.name = product_data['name']
        if 'unit_price' in product_data:
            new_product.unit_price = product_data['unit_price']
        if 'stock_type' in product_data:
            new_product.stock_type = product_data['stock_type']
        new_product.save()
        return 'Success!', 200
    except Exception as e:
        print('error:', e, file=sys.stderr)
        return 'Failed!', 400

# READ
@app.route("/product/<id>", methods=['GET'])
def get_product(id):
    try:
        print('id:', id, file=sys.stderr)
        if (id == '0'):
            print('masuk id 0', file=sys.stderr)
            products = Product.objects
        else:
            print('masuk specific id', file=sys.stderr)
            products = Product.objects(id=ObjectId(id))
        product_data = []
        for product in products:
            product_data.append({
                'name': product.name,
                'unit_price': product.unit_price,
                'stock_type': product.stock_type, 
            })
            
        return jsonify(product_data), 200
    except Exception as e:
        print('error:', e, file=sys.stderr)
        return 'Failed!', 400

# UPDATE
@app.route("/product/update/<id>", methods=['PUT'])
def update_product(id):
    try:
        print('id:', id, file=sys.stderr)
        product = Product.objects(id=ObjectId(id))
        if product:
            print('json:', request.json, file=sys.stderr)
            json_data = request.json
            for key in json_data:
                print('key:', key, file=sys.stderr)
                if key == 'name':
                    product.update_one(set__name=json_data['name'])
                elif key == 'unit_price':
                    product.update_one(set__unit_price=json_data['unit_price'])
                elif key == 'stock_type':
                    product.update_one(set__stock_type=json_data['stock_type'])

            res = []
            for p in product:
                res.append({
                    'name': p.name,
                    'unit_price': p.unit_price,
                    'stock_type': p.stock_type,
                })
            return jsonify(res), 200
        else:
            return 'Invalid ID!', 400
    except Exception as e:
        print('error:', e, file=sys.stderr)
        return 'Failed!', 400

# DELETE
@app.route("/product/delete/<id>", methods=['DELETE'])
def delete_product(id):
    try:
        print('id:', id, file=sys.stderr)
        product = Product.objects(id=ObjectId(id))
        if product:
            for p in product:
                p.delete()
            return 'Success delete product id: ' + id, 200
        else:
            return 'Invalid ID', 400
    except Exception as e:
        print('error:', e, file=sys.stderr)
        return 'Failed!', 400

# CRUD SALES
# Create
@app.route("/sales", methods=['POST'])
def create_sales():
    sales_data = json.loads(request.data)
    try:
        # customer object
        # get data sales
        new_sales = Sales()
        if 'customer_id' in sales_data:
            customer_id = sales_data['customer_id']
            customer = Customer.objects(id=ObjectId(customer_id)).first()
            new_sales.customer_id = customer
        if 'product_id' in sales_data:
            product_id = sales_data['product_id']
            product = Product.objects(id=ObjectId(product_id)).first()
            unit_price = product.unit_price
            new_sales.product_id = product
            if unit_price:
                new_sales.unit_price = unit_price
            else:
                new_sales.unit_price = 0
        if 'qty' in sales_data:
            new_sales.qty = sales_data['qty']
        else:
            new_sales.qty = 0
        new_sales.total_price = new_sales.qty * new_sales.unit_price
        new_sales.save()
        return 'Success!', 200
    except Exception as e:
        print('error:', e, file=sys.stderr)
        return 'Failed!', 400

# READ
@app.route("/sales/<id>", methods=['GET'])
def get_sales(id):
    try:
        print('id:', id, file=sys.stderr)
        if (id == '0'):
            print('masuk id 0', file=sys.stderr)
            sales = Sales.objects
        else:
            print('masuk specific id', file=sys.stderr)
            sales = Sales.objects(id=ObjectId(id))
        sales_data = []
        for sale in sales:
            customer_data = sale.customer_id.to_json()
            customer_data = json.loads(customer_data)
            product_data = sale.product_id.to_json()
            product_data = json.loads(product_data)
            sales_data.append({
                'customer_id': customer_data,
                'product_id': product_data,
                'qty': sale.qty,
                'unit_price': sale.unit_price,
                'total_price': sale.total_price,
            })
            
        return jsonify(sales_data), 200
    except Exception as e:
        print('error:', e, file=sys.stderr)
        return 'Failed!', 400

# UPDATE
@app.route("/sales/update/<id>", methods=['PUT'])
def update_sales(id):
    try:
        print('id:', id, file=sys.stderr)
        sales = Sales.objects(id=ObjectId(id)).first()
        if sales:
            print('json:', request.json, file=sys.stderr)
            json_data = request.json
            for key in json_data:
                print('key:', key, file=sys.stderr)
                if key == 'customer_id':
                    customer_id = json_data['customer_id']
                    customer = Customer.objects(id=ObjectId(customer_id)).first()
                    sales.customer_id = customer
                elif key == 'product_id':
                    product_id = json_data['product_id']
                    product = Product.objects(id=ObjectId(product_id)).first()
                    unit_price = product.unit_price
                    sales.product_id = product
                    sales.unit_price = unit_price
                elif key == 'qty':
                    sales.qty = json_data['qty']
            sales.total_price = sales.qty * sales.unit_price
            sales.save()
            sales_json = sales.to_json()
            sales_json = json.loads(sales_json)
            return jsonify(sales_json), 200
        else:
            return 'Invalid ID!', 400
    except Exception as e:
        print('error:', e, file=sys.stderr)
        return 'Failed!', 400


# DELETE
@app.route("/sales/delete/<id>", methods=['DELETE'])
def delete_sales(id):
    try:
        print('id:', id, file=sys.stderr)
        sales = Sales.objects(id=ObjectId(id))
        if sales:
            for s in sales:
                s.delete()
            return 'Success delete sales id: ' + id, 200
        else:
            return 'Invalid ID', 400
    except Exception as e:
        print('error:', e, file=sys.stderr)
        return 'Failed!', 400