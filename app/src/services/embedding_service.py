from sentence_transformers import SentenceTransformer

"""
    Modelo de embedding utilizado para codificar os documentos e consultas
"""
minilm_l6_v2 = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')