# session_manager.py
import json
import os
from database import add_bookmark, save_query

SESSION_FILE = "data/session.json"

def save_session():
    # Сохраняет последние 20 запросов и все закладки
    from database import get_history, list_bookmarks
    history = get_history(limit=20)
    bookmarks = list_bookmarks()
    data = {
        "history": history,
        "bookmarks": bookmarks
    }
    os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
    with open(SESSION_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True

def load_session():
    if not os.path.exists(SESSION_FILE):
        return False
    with open(SESSION_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Восстановление истории (только в память, не в БД)
    # Для простоты – ничего не делаем, т.к. БД уже хранит всё.
    return True