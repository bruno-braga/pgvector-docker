from flask import Blueprint, jsonify, request

from models.Document import Document
from services.embedding_service import minilm_l6_v2

import services.prompt_service as prompt

import json

from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, SemanticSimilarity
from ragas import evaluate
from langchain_openai import OpenAI
from datasets import Dataset
import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

rag_bp = Blueprint('rag', __name__)

@rag_bp.route('/get_chunks/<string:query>')
def get_chunks(query):
    queries, prompt_template, system_prompt = prompt.build(query)
    chunks = Document.get_chunks(queries, minilm_l6_v2)

    return jsonify({
        'chunks': chunks
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

    get_completion_response = prompt.get_completion(formatted_prompt, system_prompt)

    response = jsonify({
        'response': get_completion_response,
        'query': query,
        'queries': queries,
        'prompt_template': prompt_template,
        'system_prompt': system_prompt,
        'chunks': chunks,
    })

    return response

@rag_bp.route('/get_reference/<string:query>')
def get_reference(query):
    reference = json.loads(prompt.generate_reference_answer(query))

    print(reference['answer'])

    return jsonify({
        'reference_answer': reference['answer']
    })

@rag_bp.route('/evaluate', methods=['POST'])
def evaluate_response():
    # Get JSON data from request body
    data = request.get_json()
    
    # Make internal request to search endpoint
    query = data['query']
    search_response = search(query)
    search_data = json.loads(search_response.get_data(as_text=True))
    
    evaluation_data = [{
        "question": data['query'],
        "answer": search_data['response'],
        "contexts": data['chunks'],
        "reference": data['reference']
    }]

    dataset = Dataset.from_list(evaluation_data)

    llm = OpenAI()

    results = evaluate(
        dataset,
        metrics=[
            LLMContextRecall(),
            Faithfulness(),
            FactualCorrectness(),
            SemanticSimilarity()
        ]
    )

    print(results)

    # Convert results to a serializable format
    serializable_results = {
        'context_recall': results['context_recall'],
        'faithfulness': results['faithfulness'],
        'factual_correctness': results['factual_correctness'],
        'semantic_similarity': results['semantic_similarity']
    }

    return jsonify({
        'rag_answer': search_data['response'],
        'results': serializable_results
    })