from flask_inertia import Inertia
from flask_sqlalchemy import SQLAlchemy

from database.db_singleton import db

from Http.Blueprints.Home import home_bp
from Http.Blueprints.Rag import rag_bp

def init_app(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(rag_bp, url_prefix='/rag')

    inertia = Inertia()
    inertia.init_app(app)

    db.init_app(app)

    return app