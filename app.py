from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Koneksi ke MongoDB
# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient('mongodb+srv://pangeranpas:pangeranpas@cluster0.kobcojh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['sales_db']

# Collections
customers = db['customers']
products = db['products']
sales = db['sales']

@app.route('/customer', methods=['POST'])
def create_customer():
    data = request.json
    name = data.get('name')
    handphone = data.get('handphone')
    if name and handphone:
        customer_id = customers.insert_one({'name': name, 'handphone': handphone}).inserted_id
        return jsonify(str(customer_id)), 201
    return jsonify({'error': 'Invalid data'}), 400

@app.route('/customer/<id>', methods=['GET'])
def get_customer(id):
    customer = customers.find_one({'_id': ObjectId(id)})
    if customer:
        customer['_id'] = str(customer['_id'])
        return jsonify(customer)
    return jsonify({'error': 'Customer not found'}), 404

@app.route('/customer/<id>', methods=['PUT'])
def update_customer(id):
    data = request.json
    name = data.get('name')
    handphone = data.get('handphone')
    if name and handphone:
        updated = customers.update_one({'_id': ObjectId(id)}, {'$set': {'name': name, 'handphone': handphone}})
        if updated.modified_count:
            return jsonify({'message': 'Customer updated'})
        return jsonify({'error': 'Customer not found'}), 404
    return jsonify({'error': 'Invalid data'}), 400

@app.route('/customer/<id>', methods=['DELETE'])
def delete_customer(id):
    deleted = customers.delete_one({'_id': ObjectId(id)})
    if deleted.deleted_count:
        return jsonify({'message': 'Customer deleted'})
    return jsonify({'error': 'Customer not found'}), 404

@app.route('/product', methods=['POST'])
def create_product():
    data = request.json
    name = data.get('name')
    unit_price = data.get('unit_price')
    stock = data.get('stock')
    if name and unit_price is not None and stock is not None:
        product_id = products.insert_one({'name': name, 'unit_price': unit_price, 'stock': stock}).inserted_id
        return jsonify(str(product_id)), 201
    return jsonify({'error': 'Invalid data'}), 400

@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = products.find_one({'_id': ObjectId(id)})
    if product:
        product['_id'] = str(product['_id'])
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    data = request.json
    name = data.get('name')
    unit_price = data.get('unit_price')
    stock = data.get('stock')
    if name and unit_price is not None and stock is not None:
        updated = products.update_one({'_id': ObjectId(id)}, {'$set': {'name': name, 'unit_price': unit_price, 'stock': stock}})
        if updated.modified_count:
            return jsonify({'message': 'Product updated'})
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({'error': 'Invalid data'}), 400

@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    deleted = products.delete_one({'_id': ObjectId(id)})
    if deleted.deleted_count:
        return jsonify({'message': 'Product deleted'})
    return jsonify({'error': 'Product not found'}), 404

@app.route('/sales', methods=['POST'])
def create_sales():
    data = request.json
    customer_id = data.get('customer_id')
    product_id = data.get('product_id')
    qty = data.get('qty')
    
    if not all([customer_id, product_id, qty]):
        return jsonify({'error': 'Invalid data'}), 400
    
    customer = customers.find_one({'_id': ObjectId(customer_id)})
    product = products.find_one({'_id': ObjectId(product_id)})
    
    if not customer or not product:
        return jsonify({'error': 'Customer or Product not found'}), 404
    
    unit_price = product['unit_price']
    total_price = unit_price * qty
    
    sales_id = sales.insert_one({
        'customer_id': ObjectId(customer_id),
        'product_id': ObjectId(product_id),
        'unit_price': unit_price,
        'qty': qty,
        'total_price': total_price
    }).inserted_id
    
    # Update stock product
    new_stock = product['stock'] - qty
    if new_stock < 0:
        return jsonify({'error': 'Insufficient stock'}), 400
    products.update_one({'_id': ObjectId(product_id)}, {'$set': {'stock': new_stock}})
    
    return jsonify(str(sales_id)), 201

@app.route('/sales/<id>', methods=['GET'])
def get_sales(id):
    sale = sales.find_one({'_id': ObjectId(id)})
    if sale:
        sale['_id'] = str(sale['_id'])
        sale['customer_id'] = str(sale['customer_id'])
        sale['product_id'] = str(sale['product_id'])
        return jsonify(sale)
    return jsonify({'error': 'Sales not found'}), 404

@app.route('/sales/<id>', methods=['PUT'])
def update_sales(id):
    data = request.json
    customer_id = data.get('customer_id')
    product_id = data.get('product_id')
    qty = data.get('qty')
    
    if not all([customer_id, product_id, qty]):
        return jsonify({'error': 'Invalid data'}), 400
    
    customer = customers.find_one({'_id': ObjectId(customer_id)})
    product = products.find_one({'_id': ObjectId(product_id)})
    
    if not customer or not product:
        return jsonify({'error': 'Customer or Product not found'}), 404
    
    unit_price = product['unit_price']
    total_price = unit_price * qty
    
    updated = sales.update_one(
        {'_id': ObjectId(id)},
        {'$set': {
            'customer_id': ObjectId(customer_id),
            'product_id': ObjectId(product_id),
            'unit_price': unit_price,
            'qty': qty,
            'total_price': total_price
        }}
    )
    
    if updated.modified_count:
        return jsonify({'message': 'Sales updated'})
    return jsonify({'error': 'Sales not found'}), 404

@app.route('/sales/<id>', methods=['DELETE'])
def delete_sales(id):
    sale = sales.find_one({'_id': ObjectId(id)})
    if not sale:
        return jsonify({'error': 'Sales not found'}), 404
    
    product_id = sale['product_id']
    qty = sale['qty']
    
    deleted = sales.delete_one({'_id': ObjectId(id)})
    if deleted.deleted_count:
        # Update stock product
        product = products.find_one({'_id': ObjectId(product_id)})
        new_stock = product['stock'] + qty
        products.update_one({'_id': ObjectId(product_id)}, {'$set': {'stock': new_stock}})
        
        return jsonify({'message': 'Sales deleted'})
    return jsonify({'error': 'Sales not found'}), 404

@app.route('/customers', methods=['GET'])
def list_customers():
    all_customers = customers.find()
    return jsonify([{'_id': str(customer['_id']), 'name': customer['name'], 'handphone': customer['handphone']} for customer in all_customers])

@app.route('/products', methods=['GET'])
def list_products():
    all_products = products.find()
    return jsonify([{'_id': str(product['_id']), 'name': product['name'], 'unit_price': product['unit_price'], 'stock': product['stock']} for product in all_products])

@app.route('/sales', methods=['GET'])
def list_sales():
    all_sales = sales.find()
    return jsonify([{
        '_id': str(sale['_id']),
        'customer_id': str(sale['customer_id']),
        'product_id': str(sale['product_id']),
        'unit_price': sale['unit_price'],
        'qty': sale['qty'],
        'total_price': sale['total_price']
    } for sale in all_sales])

if __name__ == '__main__':
    app.run(debug=True)