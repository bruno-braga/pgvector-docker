from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector

import db
import parser

register_vector(db.conn)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

title, sentences = parser.extract_arxiv_content("./tosrag.html")

embeddings = model.encode(sentences)

data = []
for embedding, sentence in zip(embeddings, sentences):
    embedding_list = embedding.tolist()
    data_tuple = (sentence, embedding_list)
    data.append(data_tuple)

db.insert_items(data)