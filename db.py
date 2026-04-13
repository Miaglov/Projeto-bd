import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "petshop_db"),
            port=int(os.getenv("DB_PORT", 3306)),
            charset="utf8mb4",
            use_pure=True,
        )
        return conn
    except Error as e:
        raise RuntimeError(f"Erro ao conectar ao banco de dados: {e}")

def query_db(sql, args=(), one=False, commit=False):
    """
    Executa uma query e retorna os resultados como dicionários.
    - one=True  → retorna apenas uma linha
    - commit=True → faz commit (INSERT/UPDATE/DELETE) e retorna lastrowid
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, args)
        if commit:
            conn.commit()
            return cursor.lastrowid
        result = cursor.fetchone() if one else cursor.fetchall()
        return result
    finally:
        cursor.close()
        conn.close()
