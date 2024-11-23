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
    insert = "INSERT INTO items (text, embedding) VALUES %s"

    execute_values(
        cur,
        insert,
        data,
        template="(%s, %s::vector)",
        page_size=1000,
        fetch=False
    )

    conn.commit()
    conn.close()


def get_items(queries, model):
    encoded_queries = []
    for query_ in queries:
        query_embedding = model.encode(query_)
        vector_str = f"'[{','.join(map(str, query_embedding))}]'::vector"

        encoded_queries.append(vector_str)

    distance_comparisons = []
    for vec in encoded_queries:
        comparison = f"embedding <=> {vec}"
        distance_comparisons.append(comparison)

    distance_clause = f"LEAST({', '.join(distance_comparisons)})"

    cur.execute(
        f"""
        SELECT DISTINCT text, {distance_clause} as distance
        FROM items 
        ORDER BY distance
        LIMIT 10
        """
    )

    return cur.fetchall()

