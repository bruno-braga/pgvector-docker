from flask import Blueprint, jsonify

from models.Document import Document

rag_bp = Blueprint('rag', __name__)

@rag_bp.route('/get_chunks')
def get_chunks():
    return jsonify({
        'documents': [doc.to_dict() for doc in Document.query.limit(10).all()]
    })
