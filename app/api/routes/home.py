from flask import Blueprint, jsonify

home_bp = Blueprint('home', __name__)

@home_bp.route('/')  # Add root route
def index():
    return jsonify({"message": "Root page"})

@home_bp.route('/home')
def home():
    return jsonify({"message": "Hello, World!"})