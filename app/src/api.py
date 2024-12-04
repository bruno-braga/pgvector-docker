from flask_inertia import Inertia

from Http.Blueprints.Home import home_bp

def init_app(app):
    app.register_blueprint(home_bp)

    inertia = Inertia()
    inertia.init_app(app)

    return app