from pymongo import MongoClient

# Replace with your actual MongoDB Atlas credentials and database name
# client = MongoClient('mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority')
client = MongoClient('mongodb+srv://pangeranpas:pangeranpas@cluster0.kobcojh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client['sales_db']

# Collections
customers = db['customers']
products = db['products']
sales = db['sales']

# Insert dummy customers
customer_data = [
    {'name': 'John Doe', 'handphone': '1234567890'},
    {'name': 'Jane Smith', 'handphone': '0987654321'},
    {'name': 'Alice Johnson', 'handphone': '5551234567'}
]

customer_ids = customers.insert_many(customer_data).inserted_ids
print(f'Inserted customers: {customer_ids}')

# Insert dummy products
product_data = [
    {'name': 'Product A', 'unit_price': 10.0, 'stock': 100},
    {'name': 'Product B', 'unit_price': 20.0, 'stock': 150},
    {'name': 'Product C', 'unit_price': 15.0, 'stock': 200}
]

product_ids = products.insert_many(product_data).inserted_ids
print(f'Inserted products: {product_ids}')

# Insert dummy sales
sales_data = [
    {
        'customer_id': customer_ids[0],
        'product_id': product_ids[0],
        'unit_price': 10.0,
        'qty': 2,
        'total_price': 20.0
    },
    {
        'customer_id': customer_ids[1],
        'product_id': product_ids[1],
        'unit_price': 20.0,
        'qty': 1,
        'total_price': 20.0
    },
    {
        'customer_id': customer_ids[2],
        'product_id': product_ids[2],
        'unit_price': 15.0,
        'qty': 3,
        'total_price': 45.0
    }
]

sales_ids = sales.insert_many(sales_data).inserted_ids
print(f'Inserted sales: {sales_ids}')