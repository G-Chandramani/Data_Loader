from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_type = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20), nullable=False)

# Create the database and the Product table
with app.app_context():  # Ensure the context is set before creating the tables
    db.create_all()

# Route to serve the homepage (index)
@app.route('/')
def index():
    return render_template('index.html')

# Route to upload CSV file and perform CRUD operations
@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Read CSV file using pandas
    data = pd.read_csv(file)
    
    # Perform CRUD (Create) operation - Insert each row in the database
    for _, row in data.iterrows():
        product = Product(
            product_name=row['product_name'], 
            product_type=row['product_type'], 
            unit=row['unit']
        )
        db.session.add(product)
    db.session.commit()

    return jsonify({'message': 'File uploaded and data inserted successfully'}), 200

# Route to read all products (Read)
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'product_name': p.product_name, 
        'product_type': p.product_type, 
        'unit': p.unit
    } for p in products]), 200

# Route to update a product by ID (Update)
@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    data = request.get_json()
    
    # Update product details
    product.product_name = data.get('product_name', product.product_name)
    product.product_type = data.get('product_type', product.product_type)
    product.unit = data.get('unit', product.unit)

    db.session.commit()
    return jsonify({'message': 'Product updated successfully'}), 200

# Route to delete a product by ID (Delete)
@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
