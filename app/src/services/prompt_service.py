import os
import json
import yaml
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_completion(prompt, system_prompt, model="gpt-4o-mini", json_format=False):
    """
    Obtém uma resposta do modelo de linguagem usando a API OpenAI.

    Args:
        prompt (str): O prompt principal a ser enviado ao modelo
        system_prompt (str): O prompt de sistema que define o comportamento do modelo
        model (str, optional): Nome do modelo a ser usado. Padrão é "gpt-4o-mini"
        json_format (bool, optional): Se True, força a resposta em formato JSON. Padrão é False

    Returns:
        str: A resposta gerada pelo modelo
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0,
        max_tokens=500,
        response_format={"type": "json_object"} if json_format else None
    )
    
    return response.choices[0].message.content

def build(query):
    """
    Constrói os prompts e consultas necessários para o sistema RAG.

    Parâmetros
    ----------
    query : str
        A consulta original do usuário

    Retorna
    -------
    tuple
        Uma tupla contendo três elementos:
        - queries (list): Lista de consultas expandidas e processadas
        - prompt_template (str): Template do prompt a ser usado
        - system_prompt (str): Prompt do sistema que define o comportamento do modelo

    Detalhes
    --------
    Esta função:
    1. Carrega os templates de prompt do arquivo YAML
    2. Expande a consulta original em múltiplas variações
    3. Processa as respostas fictícias para enriquecer a busca
    """

    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, "prompt_template.yml")
    
    with open(template_path, "r") as file:
        prompts = yaml.safe_load(file)
    
    system_prompt = prompts["System_Prompt"]
    prompt_template = prompts["Prompt"]
    
    prompt = prompts["Prompt_Expansao"].format(query=query)
    
    response = get_completion(prompt, "", json_format=True)
    
    response_json = json.loads(response)
    queries = response_json['termos']
    respostas = response_json['respostas_ficticias']
    
    queries = queries + respostas
    
    return queries, prompt_template, system_prompt

def generate_reference_answer(query):
    """
    Gera uma resposta de referência para uma determinada query.

    Parâmetros
    ----------
    query : str
        A consulta para a qual se deseja gerar uma resposta de referência

    Retorna
    -------
    str
        Uma string JSON contendo:
        - answer: A resposta de referência gerada pelo modelo

    Detalhes
    --------
    A função cria um prompt especializado que:
    1. Define o contexto como especialista em PLN
    2. Solicita uma resposta para a consulta
    3. Força o formato de saída em JSON
    """

    prompt = f"""
        gere uma resposta para a pergunta: {query}

        A saida deve ser em formato JSON com o seguinte formato:

        {{
            "answer": "resposta"
        }}
    """

    return get_completion(prompt, "", json_format=True)
