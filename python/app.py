import tqdm
import numpy as np
from PyPDF2 import PdfReader
from psycopg2.extras import Json
from pgvector.psycopg2 import register_vector
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

import db


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

cur = db.conn.cursor()
register_vector(db.conn)

reader = PdfReader("./files/artigo_exemplo.pdf")
    
text = ""

for page in reader.pages:
    text += page.extract_text() + "\n"
        
text.split("\n")[100:105]


def merge_lines(text):
    merged = []
    current_sentence = ""
    
    for line in text:
        line = line.strip()
        if not line:
            continue
            
        if current_sentence:
            line = ' ' + line
            
        current_sentence += line
        
        if ". " in current_sentence:
            parts = current_sentence.split(". ")
            for part in parts[:-1]:
                merged.append(part + ".")
            current_sentence = parts[-1]
    
    if current_sentence:
        merged.append(current_sentence)
        
    return merged

sentences = merge_lines(text.split("\n"))
# sentences[0:5]

embeddings = model.encode(sentences)

insert = "INSERT INTO embeddings (value) VALUES (%s::vector)"

for idx, embedding in tqdm(enumerate(embeddings), total=len(embeddings)):
    embedding_list = embedding.tolist()
    cur.execute(insert, (embedding_list,))

db.conn.commit()
db.conn.close()