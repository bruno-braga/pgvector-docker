from flask_inertia import Inertia
from flask_sqlalchemy import SQLAlchemy

from database.db_singleton import db

from Http.Blueprints.Home import home_bp
from Http.Blueprints.Rag import rag_bp
from Http.Blueprints.Report import report_bp

def init_app(app):
    """
        Params
        ______
        - app: Aplicação flask a ser inicializada


        Inicializa a aplicação registrando:
        - Rotas especificas para cada modulo do sistema(blueprints)
        - Inertia para renderização da interface
        - Banco de dados

        returns
        _______
        - app: Aplicação flask inicializada
    """

    app.register_blueprint(home_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(rag_bp, url_prefix='/rag')

    inertia = Inertia()
    inertia.init_app(app)

    db.init_app(app)

    return app