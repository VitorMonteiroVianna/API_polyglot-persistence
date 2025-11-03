import psycopg2
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

USER = os.getenv("USER")               # ex: postgres.greohsxqhprfponfpfvk
PASSWORD = os.getenv("PASSWORD")       # ex: FeiTriste123
HOST = os.getenv("HOST")               # ex: aws-1-us-east-1.pooler.supabase.com
PORT = os.getenv("PORT")               # ex: 6543
DBNAME = os.getenv("DBNAME")           # ex: postgres

try:
    conn = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME,
        sslmode="require"   # obrigatório para o Pooler
    )

    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")
    print("Connection successful! Current time:", cursor.fetchone())

    cursor.close()
    conn.close()
    print("Connection closed.")

except Exception as e:
    print("Failed to connect:", e)
