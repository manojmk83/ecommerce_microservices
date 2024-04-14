# app.py (main application file)
from models import db
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

secret_key = os.urandom(32).hex()


app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secret_key
db.init_app(app)
with app.app_context():
    db.create_all()

# Extensions
# db = SQLAlchemy(app)
jwt = JWTManager(app)

# Import blueprints
from auth_service.auth_service import auth_bp
from product_service.product_service import product_bp
from order_service.order_service import order_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(order_bp)

if __name__ == "__main__":
    app.run(debug=True)
