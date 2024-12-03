from flask import Flask, jsonify, request
from flask_inertia import Inertia
from flask.typing import ResponseReturnValue
from flask_inertia import render_inertia

from sentence_transformers import SentenceTransformer
import os
import yaml

import prompt
import db

app = Flask(__name__)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

app.config['SECRET_KEY'] = "secret!"
app.config['INERTIA_TEMPLATE'] = "base.html"

inertia = Inertia()
inertia.init_app(app)

@app.route('/')
@app.route('/home')
def home():
    return render_inertia('Home')
    
@app.route('/api/get_prompt')
def get_prompt():
    try:
        with open('prompt_template.yml', 'r') as f:
            prompt_data = yaml.safe_load(f)
        return jsonify(prompt_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fetch_chunks')
def get_chunks():
    search = request.args.get('search')
    print(search)

    queries, prompt_template, system_prompt = prompt.build(search)
    chunks = db.get_items(queries, model)

    all_docs = []
    for result in chunks:
        all_docs.append(result[0])

    formatted_chunks = ""
    for chunk in all_docs:
        print(chunk)
        formatted_chunks += "Titulo do artigo: " + result[2]
        formatted_chunks += "\n"
        formatted_chunks += "\n"

        formatted_chunks += f"{chunk}\n"
        formatted_chunks += "\n"

    formatted_chunks = formatted_chunks.strip()

    return jsonify({'chunks': formatted_chunks})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)