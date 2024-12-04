from flask import Flask
from api import init_app

app = Flask(__name__, template_folder='static/')

app = init_app(app)

app.config['SECRET_KEY'] = "secret!"
app.config['INERTIA_TEMPLATE'] = "base.html"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)