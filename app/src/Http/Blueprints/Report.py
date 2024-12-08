from flask import Blueprint, jsonify
from flask_inertia import render_inertia

from models.Document import Document

report_bp = Blueprint('report', __name__)

@report_bp.route('/report')
def index():
    """
    Renderiza a página de relatório que mostra o processo de avaliação
    do sistema RAG passo a passo.

    Retorna
    -------
    flask.Response
        Renderiza o componente Report com os títulos dos artigos disponíveis
        no banco de dados como propriedade.
    """
    titles = Document.get_distinct_titles()
    return render_inertia('Report', props={'titles': titles})