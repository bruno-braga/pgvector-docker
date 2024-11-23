from sentence_transformers import SentenceTransformer
import prompt
import yaml
import json
import db

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

query = "Que modelos de LLMs são avaliados e qual é o principal resultado do artigo?"
queries, prompt_template, system_prompt = prompt.build(query)

results = db.get_items(queries, model)

all_docs = []
for result in results:
    all_docs.append(result[0])

formatted_chunks = "\n".join([f"{chunk}\n" for chunk in all_docs])
formatted_prompt = prompt_template.format(chunks=formatted_chunks, query=query)

response = prompt.get_completion(formatted_prompt, system_prompt)

print(formatted_prompt)
print(response)
print(results)