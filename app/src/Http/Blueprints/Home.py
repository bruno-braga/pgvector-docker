from flask import Blueprint, jsonify
from flask_inertia import render_inertia

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
@home_bp.route('/home')
def index():
    """
        Renderiza a pagina disponibilizando
        uma interface para perguntar e ler as
        respostas através do RAG
    """	
    return render_inertia('Home')
