from flask import Flask
from api import init_app

import os

app = Flask(__name__, template_folder='static/')

app.config['SECRET_KEY'] = "secret!"
app.config['INERTIA_TEMPLATE'] = "base.html"
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app = init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)