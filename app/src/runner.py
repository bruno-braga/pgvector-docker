from flask import Flask
from api import init_app

import os

# Cria um app flask setando a pasta static/
# como caminho base para arquivos da interface
app = Flask(__name__, template_folder='static/')

# Configura chaves especificas do app
# para banco de dados, secret_key e também
# arquivo "entrypoint" da interface - base.html -
app.config['SECRET_KEY'] = os.getenv('APP_SECRET')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['INERTIA_TEMPLATE'] = "base.html"

# E por fim inicializa o app
app = init_app(app)

if __name__ == '__main__':
    # apos inicialização seta host, porta
    # e status para debug
    app.run(host='0.0.0.0', port=5000, debug=True)