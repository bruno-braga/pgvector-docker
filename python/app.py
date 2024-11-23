from PyPDF2 import PdfReader

from psycopg2.extras import Json
from pgvector.psycopg2 import register_vector

from sentence_transformers import SentenceTransformer

from openai import OpenAI

import os
import yaml
import json

import db

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

cur = db.conn.cursor()

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

query = "Que modelos de LLMs são avaliados e qual é o principal resultado do artigo?"

with open("prompt_template.yml", "r") as file:
    prompts = yaml.safe_load(file)

system_prompt = prompts["System_Prompt"]
prompt_template = prompts["Prompt"]

prompt = prompts["Prompt_Expansao"].format(query=query)

response = get_completion(prompt, "", json_format=True)

response_json = json.loads(response)
queries = response_json['termos']
respostas = response_json['respostas_ficticias']

queries = queries + respostas

encoded_queries = []
for query_ in queries:
    query_embedding = model.encode(query_)
    vector_str = f"'[{','.join(map(str, query_embedding))}]'::vector"

    encoded_queries.append(vector_str)

distance_comparisons = [f"embedding <=> {vec}" for vec in encoded_queries]
distance_clause = f"LEAST({', '.join(distance_comparisons)})"

cur.execute(
    f"""
    SELECT DISTINCT text, {distance_clause} as distance
    FROM items 
    ORDER BY distance
    LIMIT 10
    """
)

results = cur.fetchall()

all_docs = []
for result in results:
    all_docs.append(result[0])

formatted_chunks = "\n".join([f"{chunk}\n" for chunk in all_docs])

prompt = prompt_template.format(chunks=formatted_chunks, query=query)

response = get_completion(prompt, system_prompt)

print(prompt)
print(response)
print(results)