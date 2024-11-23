from PyPDF2 import PdfReader

from psycopg2.extras import Json
from pgvector.psycopg2 import register_vector

from sentence_transformers import SentenceTransformer

import get_completion

import yaml
import json

import db

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

cur = db.conn.cursor()

query = "Que modelos de LLMs são avaliados e qual é o principal resultado do artigo?"

with open("prompt_template.yml", "r") as file:
    prompts = yaml.safe_load(file)

system_prompt = prompts["System_Prompt"]
prompt_template = prompts["Prompt"]

prompt = prompts["Prompt_Expansao"].format(query=query)

response = get_completion.get_completion(prompt, "", json_format=True)

response_json = json.loads(response)
queries = response_json['termos']
respostas = response_json['respostas_ficticias']

queries = queries + respostas

results = db.get_items(queries, model)

all_docs = []
for result in results:
    all_docs.append(result[0])

formatted_chunks = "\n".join([f"{chunk}\n" for chunk in all_docs])

prompt = prompt_template.format(chunks=formatted_chunks, query=query)

response = get_completion.get_completion(prompt, system_prompt)

print(prompt)

print(response)

print(results)