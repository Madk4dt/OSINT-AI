# compare_results.py
from database import get_history
from difflib import unified_diff

def compare_last_two():
    history = get_history(limit=2)
    if len(history) < 2:
        return "Недостаточно записей для сравнения (нужно минимум 2)", []
    r1, r2 = history[0][3], history[1][3]
    diff = list(unified_diff(r1.splitlines(), r2.splitlines(), lineterm=''))
    if not diff:
        return "Результаты идентичны", []
    return "\n".join(diff[:50]), []