from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector

import db

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

register_vector(db.conn)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

reader = PdfReader("./files/artigo_exemplo.pdf")
text = ""

for page in reader.pages:
    text += page.extract_text() + "\n"
        
sentences = merge_lines(text.split("\n"))

embeddings = model.encode(sentences)

data = []
for embedding, sentence in zip(embeddings, sentences):
    embedding_list = embedding.tolist()
    data_tuple = (sentence, embedding_list)
    data.append(data_tuple)

db.insert_items(data)