from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()


conn = psycopg2.connect(
    database=os.getenv('DB_DATABASE'),
    user=os.getenv('DB_USERNAME'),
    host=os.getenv('DB_HOST'),
    password=os.getenv('DB_PASSWORD'),
    port=os.getenv('DB_PORT')
)

cur = conn.cursor()
cur.execute("""SELECT * FROM items;""")

print(cur.fetchall())

conn.close()