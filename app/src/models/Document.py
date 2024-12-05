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
