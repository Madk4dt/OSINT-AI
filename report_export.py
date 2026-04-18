# report_export.py
import json
import csv
from datetime import datetime
from database import get_history

def export_json(filename=None):
    if not filename:
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    history = get_history(limit=100)
    data = [{"type": h[0], "value": h[1], "timestamp": h[2], "result": h[3]} for h in history]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return f"Экспортировано в {filename}", []

def export_csv(filename=None):
    if not filename:
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    history = get_history(limit=100)
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "Value", "Timestamp", "Result"])
        writer.writerows(history)
    return f"Экспортировано в {filename}", []