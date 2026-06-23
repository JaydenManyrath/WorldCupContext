import sqlite3

DB_NAME = 'worldcup.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_database():
    with get_connection() as conn:
        with open('Schema.sql', 'r') as f:
            conn.executescript(f.read())

def execute_query(query, params=()):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

def fetch_all(query, params=()):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def fetch_one(query, params=()):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()