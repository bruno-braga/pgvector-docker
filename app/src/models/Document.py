from sqlalchemy import Column, Integer, String, Float, select
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import VECTOR

from database.db_singleton import db

class Document(db.Model):
    """
    Modelo que representa um documento no banco de dados.

    Atributos
    ---------
    id : int
        Identificador único do documento
    text : str
        Texto do documento
    article_title : str
        Título do artigo ao qual o documento pertence
    embedding : VECTOR
        Vetor de embedding do documento
    """

    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    text = Column(String)
    article_title = Column(String)
    embedding = Column(VECTOR)

    def to_dict(self):
        """
        Converte o documento em um dicionário.

        Retorna
        -------
        dict
            Dicionário contendo os atributos do documento:
            - id: Identificador único
            - text: Texto do documento
            - article_title: Título do artigo
            - embedding: Vetor de embedding (convertido para lista se existir)
        """
        return {
            'id': self.id,
            'text': self.text,
            'article_title': self.article_title,
            'embedding': self.embedding.tolist() if self.embedding is not None else None
        }

    @classmethod
    def get_distinct_titles(cls):
        """
        Recupera todos os títulos únicos de artigos.

        Retorna
        -------
        list
            Lista de títulos únicos de artigos no banco de dados
        """
        results = db.session.query(cls.article_title).distinct().all()
        return [result[0] for result in results]

    @classmethod    
    def get_limit10(cls):
        """
        Recupera os 10 primeiros documentos do banco de dados.

        Retorna
        -------
        list
            Lista contendo os 10 primeiros documentos
        """
        return cls.query.limit(10).all()

    @classmethod
    def get_chunks(cls, queries, model, distance_metric='l2'):
        """
        Recupera trechos de documentos relevantes baseados em consultas.

        Parâmetros
        ----------
        queries : list
            Lista de strings contendo as consultas
        model : object
            Modelo de embedding a ser usado para codificar as consultas
        distance_metric : str, opcional
            Métrica de distância a ser usada ('l2' ou 'cosine', padrão é 'l2')

        Retorna
        -------
        list
            Lista de dicionários contendo os trechos mais relevantes, cada um com:
            - text: Texto do trecho
            - article_title: Título do artigo
            - embedding: Vetor de embedding do trecho
        """
        results = []

        # Define a função de distância com base na métrica escolhida
        if distance_metric == 'l2':
            distance_metric_function = cls.embedding.l2_distance
        else:
            distance_metric_function = cls.embedding.cosine_distance

        # Para cada termo
        for query_ in queries:
            # Recupera os documentos mais relevantes ordenados pela distância
            # do embedding do termo com o embedding do documento
            query_results = db.session.query(
                cls.text.label('text'),
                cls.article_title.label('article_title'),
                cls.embedding.label('embedding')
            ).order_by(
                distance_metric_function(model.encode(query_).tolist())
            ).limit(10).all()

            # Serializa os resultados em um formato JSON
            serializable_results = [
                {
                    'text': row._mapping['text'],
                    'article_title': row._mapping['article_title'],
                    'embedding': row._mapping['embedding'].tolist() if row._mapping['embedding'] is not None else None
                }
                for row in query_results
            ]

            # Adiciona os resultados serializados à lista principal
            results.extend(serializable_results)
            
        return results