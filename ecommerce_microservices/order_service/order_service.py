# order_service.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from models import Order
from models import db, Product
order_bp = Blueprint('order', __name__)
@order_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    # Create a new order for the authenticated user
    user_id = get_jwt_identity()

    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Check if required fields are provided
    if not product_id or not quantity:
        return jsonify({'message': 'Product ID and quantity are required'}), 400

    # Check if the product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Create a new order object
    new_order = Order(user_id=user_id, product_id=product_id, quantity=quantity)

    # Add the new order to the database
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order created successfully', 'order_id': new_order.id}), 201

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    # Retrieve an order by its ID
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'message': 'Order not found'}), 404

    # Check if the order belongs to the authenticated user
    if order.user_id != get_jwt_identity():
        return jsonify({'message': 'Unauthorized access to the order'}), 403

    return jsonify(order.serialize())

@order_bp.route('/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    # Update an existing order
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'message': 'Order not found'}), 404

    # Check if the order belongs to the authenticated user
    if order.user_id != get_jwt_identity():
        return jsonify({'message': 'Unauthorized access to the order'}), 403

    data = request.json
    quantity = data.get('quantity')

    if quantity:
        order.quantity = quantity

    db.session.commit()

    return jsonify({'message': 'Order updated successfully'})

@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    # Delete an existing order
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'message': 'Order not found'}), 404

    # Check if the order belongs to the authenticated user
    if order.user_id != get_jwt_identity():
        return jsonify({'message': 'Unauthorized access to the order'}), 403

    db.session.delete(order)
    db.session.commit()

    return jsonify({'message': 'Order deleted successfully'})
