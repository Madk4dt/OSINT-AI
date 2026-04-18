# database.py
import sqlite3
import os
from datetime import datetime
from config import DB_PATH

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_type TEXT,
        query_value TEXT,
        timestamp TEXT,
        result TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

def save_query(qtype, qvalue, result):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    ts = datetime.now().isoformat()
    c.execute("INSERT INTO queries (query_type, query_value, timestamp, result) VALUES (?,?,?,?)",
              (qtype, qvalue, ts, result))
    conn.commit()
    conn.close()

def get_history(limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT query_type, query_value, timestamp, result FROM queries ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def add_bookmark(title, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    ts = datetime.now().isoformat()
    c.execute("INSERT INTO bookmarks (title, content, timestamp) VALUES (?,?,?)", (title, content, ts))
    conn.commit()
    conn.close()

def list_bookmarks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, timestamp FROM bookmarks ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows