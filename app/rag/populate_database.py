from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector

import os
import db

from parser import Context

register_vector(db.conn)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

for folder in os.listdir('./articles'):
    for file in os.listdir(os.path.join('./articles', folder)):
        if file.endswith(".html"):
            context = Context(folder)
            title, sentences = context.extract(os.path.join('./articles', folder, file))

            print(title)

            embeddings = model.encode(sentences)

            data = []
            for embedding, sentence in zip(embeddings, sentences):
                embedding_list = embedding.tolist()
                data_tuple = (sentence, embedding_list, title)
                data.append(data_tuple)

            db.insert_items(data)

db.clean_section_chunks()
