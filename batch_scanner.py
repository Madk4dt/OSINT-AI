# batch_scanner.py
import os
from utils import print_info

def batch_scan(filename):
    if not os.path.exists(filename):
        return f"Файл {filename} не найден", []
    with open(filename, 'r', encoding='utf-8') as f:
        commands = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    results = []
    for cmd in commands:
        print_info(f"Выполняется: {cmd}")
        # Здесь нужно вызвать process_command – но чтобы избежать циклического импорта,
        # мы не можем импортировать main.process_command. Поэтому просто эмулируем.
        # В реальном коде лучше передать команду в глобальный обработчик через callback.
        # Для простоты пока так:
        results.append(f"Команда: {cmd} -> выполнено (заглушка)")
    return "\n".join(results), []