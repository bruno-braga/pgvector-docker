from flask import Blueprint, jsonify, request

from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, SemanticSimilarity
from ragas import evaluate
from langchain_openai import OpenAI
from datasets import Dataset

from models.Document import Document

from services.embedding_service import minilm_l6_v2
import services.prompt_service as prompt

import json
import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

rag_bp = Blueprint('rag', __name__)

@rag_bp.route('/get_chunks/<string:query>')
def get_chunks(query, distance_metric='l2'):
    """
    Recupera trechos relevantes de documentos com base na consulta fornecida.
    É utilizado em /report para mostrar o processo de evaluation passo a passo.

    Parâmetros
    ----------
    query : str
        Uma string para encontrar trechos relevantes
    distance_metric : str, opcional
        A métrica de distância a ser usada para busca por similaridade (padrão é 'l2')

    Retorna
    -------
    flask.Response
        Resposta JSON contendo:
        - chunks: Lista de trechos relevantes de documentos com seus textos e metadados
    """

    # Constroi um promp baseado na busca do usuário
    queries, prompt_template, system_prompt = prompt.build(query)

    # Busca os chunks relevantes para a consulta
    chunks = Document.get_chunks(queries, minilm_l6_v2)

    # Retorna um json com os chunks relevantes
    return jsonify({
        'chunks': chunks
    })

@rag_bp.route('/search/<string:query>')
def search(query, distance_metric='l2'):
    """
    Realiza uma operação de busca usando RAG (Retrieval-Augmented Generation).

    Parâmetros
    ----------
    query : str
        A consulta de busca do usuário
    distance_metric : str, opcional
        A métrica de distância a ser usada para busca por similaridade (padrão é 'l2')

    Retorna
    -------
    flask.Response
        Resposta JSON contendo:
        - response: Resposta gerada pela completação
        - query: Consulta original
        - queries: Consultas processadas
        - prompt_template: Template usado para o prompt
        - system_prompt: Prompt do sistema utilizado
        - chunks: Trechos de documentos recuperados
    """

    # Constroi um promp baseado na busca do usuário
    queries, prompt_template, system_prompt = prompt.build(query)

    # Busca os chunks relevantes para a consulta
    chunks = Document.get_chunks(queries, minilm_l6_v2)


    # Cria um array com o texto e titulo de artigo de cada chunk
    all_docs = []
    for chunk in chunks:
        all_docs.append(chunk['text'] + ', \n titulo dos artigos: ' + chunk['article_title'])

    # Formata o prompt para o modelo
    formatted_chunks = "\n".join([f"{chunk}\n" for chunk in all_docs])
    formatted_prompt = prompt_template.format(chunks=formatted_chunks, query=query)

    # Envia prompt para openAI para gerar a resposta
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
    """
    Gera uma resposta de referência para uma determinada consulta.
    É utilizado em /report para mostrar o processo de evaluation passo a passo
    bem como é enviada como parametro para /evaluate.

    Parâmetros
    ----------
    query : str
        A consulta para gerar uma resposta de referência

    Retorna
    -------
    flask.Response
        Resposta JSON contendo:
        - reference_answer: A resposta de referência gerada
    """

    # Gera a resposta de referência para avaliação do sistema RAG
    reference = json.loads(prompt.generate_reference_answer(query))

    # Retorna um json com a resposta de referência
    return jsonify({
        'reference_answer': reference['answer']
    })

@rag_bp.route('/evaluate', methods=['POST'])
def evaluate_response():
    """
    Avalia a resposta do sistema RAG usando múltiplas métricas.

    Realiza avaliação usando métricas de distância L2 e cosseno, comparando
    os resultados usando várias métricas de avaliação, incluindo recall de contexto,
    fidelidade, correção factual e similaridade semântica.

    Parâmetros
    ----------
    data : dict
        Dados JSON da requisição POST contendo:
        - query: A consulta de busca
        - chunks: Os trechos de contexto
        - reference: A resposta de referência

    Retorna
    -------
    flask.Response
        Resposta JSON contendo:
        - rag_answer: A resposta gerada pelo sistema RAG
        - results: Métricas de avaliação usando distância L2
        - results_cosine: Métricas de avaliação usando distância do cosseno
        
        Cada objeto de resultados contém:
        - context_recall: Pontuação para uso do contexto
        - faithfulness: Pontuação para fidelidade da resposta ao contexto
        - factual_correctness: Pontuação para precisão factual
        - semantic_similarity: Pontuação para similaridade com a referência
    """

    data = request.get_json()
    
    query = data['query']

    # chama a função search diretamente para buscar os chunks
    # utilizando distância do L2 para o calculo de similaridade
    search_l2_response = search(query)
    search_l2_data = json.loads(search_l2_response.get_data(as_text=True))

    # chama a função search diretamente para buscar os chunks
    # utilizando distância do cosseno para o calculo de similaridade
    search_cosine_response = search(query, distance_metric='cosine')
    search_cosine_data = json.loads(search_cosine_response.get_data(as_text=True))
    
    # organiza os dados para a avaliação da resposta do sistema RAG
    evaluation_data_l2 = [{
        "question": data['query'],
        "answer": search_l2_data['response'],
        "contexts": data['chunks'],
        "reference": data['reference']
    }]

    # organiza os dados para a avaliação da resposta do sistema RAG
    evaluation_data_cosine = [{
        "question": data['query'],
        "answer": search_cosine_data['response'],
        "contexts": data['chunks'],
        "reference": data['reference']
    }]

    # cria um dataset para a avaliação da resposta do sistema RAG
    dataset_l2 = Dataset.from_list(evaluation_data_l2)

    # cria um dataset para a avaliação da resposta do sistema RAG
    dataset_cosine = Dataset.from_list(evaluation_data_cosine)

    # avalia a resposta do sistema RAG
    # para dados recuperados com distância do L2
    results_l2 = evaluate(
        dataset_l2,
        metrics=[
            LLMContextRecall(),
            Faithfulness(),
            FactualCorrectness(),
            SemanticSimilarity()
        ]
    )

    # avalia a resposta do sistema RAG para dados
    # recuperados com distância do cosseno
    results_cosine = evaluate(
        dataset_cosine,
        metrics=[
            LLMContextRecall(),
            Faithfulness(),
            FactualCorrectness(),
            SemanticSimilarity()
        ]
    )

    # serializa os resultados da avaliação da resposta do sistema RAG
    serializable_results = {
        'context_recall': results_l2['context_recall'],
        'faithfulness': results_l2['faithfulness'],
        'factual_correctness': results_l2['factual_correctness'],
        'semantic_similarity': results_l2['semantic_similarity']
    }

    # serializa os resultados da avaliação da resposta do sistema RAG
    serializable_cosine = {
        'context_recall': results_cosine['context_recall'],
        'faithfulness': results_cosine['faithfulness'],
        'factual_correctness': results_cosine['factual_correctness'],
        'semantic_similarity': results_cosine['semantic_similarity']
    }

    # retorna um json com os resultados da avaliação da resposta do sistema RAG
    return jsonify({
        'rag_answer_l2': search_l2_data['response'],
        'rag_answer_cosine': search_cosine_data['response'],
        'results': serializable_results,
        'results_cosine': serializable_cosine
    })
