# src/db_utils.py
import sqlite3

DATABASE_PATH = "database/gerenciamento_contatos.db"

def get_connection():
    """Retorna uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def execute_query(query, params=()):
    """Executa uma query com parâmetros opcionais."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
