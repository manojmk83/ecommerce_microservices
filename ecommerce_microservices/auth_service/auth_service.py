# auth_service.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models import db
from models import User as user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # Extract user data from the request
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if the username or password is missing
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Check if the username already exists
    existing_user = user.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409
    hashed_password = generate_password_hash(password)
    # Create a new user object
    new_user = user(username=username, password=hashed_password)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Generate a JWT token for the registered user
    access_token = create_access_token(identity=new_user.id)

    # Return the JWT token as a response
    return jsonify({'access_token': access_token}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    # Extract user credentials from the request
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if both username and password are provided
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Query the database to find the user by username
    current_user = user.query.filter_by(username=username).first()

    # Check if the user exists
    if not current_user:
        return jsonify({'message': 'User not found'}), 404

    # Check if the provided password matches the user's password
    if not check_password_hash(current_user.password, password):
        return jsonify({'message': 'Incorrect password'}), 401

    # Generate JWT token for the authenticated user
    access_token = create_access_token(identity=current_user.id)

    # Return the JWT token as a response
    return jsonify({'access_token': access_token}), 200
