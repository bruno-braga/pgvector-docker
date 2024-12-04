from flask import Blueprint, jsonify
from flask_inertia import render_inertia

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def index():
    return render_inertia('Home')