# product_service.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Product
from models import db
product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['POST'])
def create_product():
    # Create a new product
    data = request.json
    name = data.get('name')
    price = data.get('price')

    # Check if required fields are provided
    if not name or not price:
        return jsonify({'message': 'Name and price are required'}), 400

    # Create a new product object
    new_product = Product(name=name, price=price)

    # Add the new product to the database
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product created successfully', 'product_id': new_product.id}), 201

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # Retrieve a product by its ID
    product = Product.query.get(product_id)

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    return jsonify(product.serialize())

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    # Update an existing product
    product = Product.query.get(product_id)

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    data = request.json
    name = data.get('name')
    price = data.get('price')

    if name:
        product.name = name
    if price:
        product.price = price

    db.session.commit()

    return jsonify({'message': 'Product updated successfully'})

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Delete an existing product
    product = Product.query.get(product_id)

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted successfully'})