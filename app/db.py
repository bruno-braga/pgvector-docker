import os
from dotenv import load_dotenv

import psycopg2
from psycopg2.extras import execute_values

load_dotenv()

conn = psycopg2.connect(
    database=os.getenv('DB_DATABASE'),
    user=os.getenv('DB_USERNAME'),
    host=os.getenv('DB_HOST'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)

cur = conn.cursor()

def insert_items(data):
    insert = "INSERT INTO items (text, embedding, article_title) VALUES %s"

    execute_values(
        cur,
        insert,
        data,
        template="(%s, %s::vector, %s)",
        page_size=1000,
        fetch=False
    )

    conn.commit()
    # conn.close()


def get_items(queries, model):
    for query_ in queries:
        cur.execute(
            """
            SELECT text, embedding, article_title
            FROM items
            ORDER BY embedding <-> %s::vector
            LIMIT 10
            """,
            (model.encode(query_).tolist(),)
        )

        
    return cur.fetchall()

