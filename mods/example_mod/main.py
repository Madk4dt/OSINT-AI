# mods/example_mod/main.py
"""
Пример мода для OSINT AI.
Добавляет команду example, которая просто выводит переданный аргумент.

Example mod for OSINT AI.
Adds the 'example' command that simply prints the argument.
"""

def register(register_command, print_success, print_info):
    """
    Регистрирует команду мода.
    Registers the mod command.
    """
    def example_handler(arg):
        # Обработчик должен вернуть (текст результата, список источников)
        # Handler must return (result text, list of sources)
        return (f"Пример мода: вы ввели '{arg}'\n"
                f"Это демонстрация работы модульной системы.\n"
                f"Example mod: you entered '{arg}'\n"
                f"This demonstrates the mod system."), []

    # Регистрируем команду с регулярным выражением
    register_command(r"^example\s+(.+)$", example_handler)

    print_success("Example mod: команда 'example' зарегистрирована / command registered")
    print_info("Используйте: example <любой текст> / Usage: example <any text>")
