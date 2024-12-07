from sqlalchemy import Column, Integer, String, Float, select
from sqlalchemy.ext.declarative import declarative_base
from pgvector.sqlalchemy import VECTOR

from database.db_singleton import db

class Document(db.Model):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    text = Column(String)
    article_title = Column(String)
    embedding = Column(VECTOR)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'article_title': self.article_title,
            'embedding': self.embedding.tolist() if self.embedding is not None else None
        }

    @classmethod
    def get_distinct_titles(cls):
        results = db.session.query(cls.article_title).distinct().all()
        return [result[0] for result in results]

    @classmethod    
    def get_limit10(cls):
        return cls.query.limit(10).all()

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'article_title': self.article_title
        }

    @classmethod
    def get_chunks(cls, queries, model, distance_metric='l2'):
        results = []

        if distance_metric == 'l2':
            distance_metric_function = cls.embedding.l2_distance
        else:
            distance_metric_function = cls.embedding.cosine_distance

        for query_ in queries:
            query_results = db.session.query(
                cls.text.label('text'),
                cls.article_title.label('article_title'),
                cls.embedding.label('embedding')
            ).order_by(
                distance_metric_function(model.encode(query_).tolist())
            ).limit(10).all()
            
            serializable_results = [
                {
                    'text': row._mapping['text'],
                    'article_title': row._mapping['article_title'],
                    'embedding': row._mapping['embedding'].tolist() if row._mapping['embedding'] is not None else None
                }
                for row in query_results
            ]
            results.extend(serializable_results)
            
        return results