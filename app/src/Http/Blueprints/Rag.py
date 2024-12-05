from flask import Blueprint, jsonify, request

from models.Document import Document
from services.embedding_service import minilm_l6_v2

import services.prompt_service as prompt

rag_bp = Blueprint('rag', __name__)

@rag_bp.route('/get_chunks')
def get_chunks():
    return jsonify({
        'documents': [doc.to_dict() for doc in Document.get_limit10()]
    })

@rag_bp.route('/search/<string:query>')
def search(query):

    queries, prompt_template, system_prompt = prompt.build(query)
    chunks = Document.get_chunks(queries, minilm_l6_v2)

    all_docs = []
    for chunk in chunks:
        all_docs.append(chunk['text'] + ', \n titulo dos artigos: ' + chunk['article_title'])

    formatted_chunks = "\n".join([f"{chunk}\n" for chunk in all_docs])
    formatted_prompt = prompt_template.format(chunks=formatted_chunks, query=query)

    response = prompt.get_completion(formatted_prompt, system_prompt)

    return jsonify({
        'response': response,
        'query': query,
        'queries': queries,
        'prompt_template': prompt_template,
        'system_prompt': system_prompt,
        'chunks': chunks,
    })