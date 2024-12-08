from flask import Blueprint, jsonify
from flask_inertia import render_inertia

from models.Document import Document

report_bp = Blueprint('report', __name__)

@report_bp.route('/report')
def index():
    titles = Document.get_distinct_titles()
    return render_inertia('Report', props={'titles': titles})