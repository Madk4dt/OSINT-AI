# core/api.py
"""
Публичное API для модов OSINT AI.
Моды могут импортировать отсюда только разрешённые функции.

Public API for OSINT AI mods.
Mods can import only allowed functions from here.
"""

from utils import (
    print_success, print_error, print_info, print_warning,
    print_result, animated_print, c, t, is_valid_ip, is_valid_domain
)
from database import save_query, get_history, add_bookmark, list_bookmarks

# Словарь для регистрации команд модами
# Dictionary for registering mod commands
_registered_commands = {}

def register_command(pattern, handler):
    """
    Регистрирует команду для основного цикла.
    pattern: строка regex (как в main.COMMANDS)
    handler: callable, принимающий аргумент (match group) и возвращающий (result, sources)

    Registers a command for the main loop.
    pattern: regex string (like in main.COMMANDS)
    handler: callable taking argument (match group) and returning (result, sources)
    """
    _registered_commands[pattern] = handler

def get_registered_commands():
    """Возвращает словарь команд, зарегистрированных модами."""
    return _registered_commands.copy()

__all__ = [
    'print_success', 'print_error', 'print_info', 'print_warning',
    'print_result', 'animated_print', 'c', 't',
    'is_valid_ip', 'is_valid_domain',
    'save_query', 'get_history', 'add_bookmark', 'list_bookmarks',
    'register_command', 'get_registered_commands'
]
