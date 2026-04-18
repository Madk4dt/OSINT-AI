# core/loader.py
"""
Загрузчик модов. Сканирует папку mods/ рядом с программой или внутри exe.
Поддерживает динамическую подгрузку: моды можно добавлять/менять без перекомпиляции.

Mod loader. Scans the mods/ folder next to the program or inside the exe.
Supports dynamic loading: mods can be added/changed without recompilation.
"""

import os
import sys
import json
import importlib.util
from pathlib import Path

def get_mods_path():
    """
    Определяет путь к папке mods.
    Сначала ищет рядом с исполняемым файлом (пользовательские моды),
    затем внутри .exe (встроенные моды, если есть).

    Determines the path to the mods folder.
    First looks next to the executable (user mods),
    then inside the .exe (built-in mods if any).
    """
    # 1. Рядом с исполняемым файлом (динамическая подгрузка)
    if getattr(sys, 'frozen', False):
        exe_dir = Path(sys.executable).parent
        user_mods = exe_dir / "mods"
        if user_mods.exists():
            return user_mods
    else:
        # Режим скрипта: рядом с main.py
        script_dir = Path(__file__).parent.parent
        user_mods = script_dir / "mods"
        if user_mods.exists():
            return user_mods

    # 2. Внутри .exe (если моды были добавлены через --add-data)
    if getattr(sys, 'frozen', False):
        # PyInstaller создаёт временную папку и хранит данные в sys._MEIPASS
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass:
            builtin_mods = Path(meipass) / "mods"
            if builtin_mods.exists():
                return builtin_mods

    # 3. Ничего не найдено
    return None

def load_mods():
    """
    Загружает все моды из папки mods.
    Возвращает список метаданных загруженных модов.

    Loads all mods from the mods folder.
    Returns a list of loaded mod metadata.
    """
    mods_path = get_mods_path()
    if mods_path is None:
        print("[ModLoader] Папка mods не найдена / Mods folder not found")
        return []

    loaded = []
    for mod_dir in mods_path.iterdir():
        if not mod_dir.is_dir():
            continue
        manifest_file = mod_dir / "manifest.json"
        if not manifest_file.exists():
            print(f"[ModLoader] Пропущен {mod_dir.name}: нет manifest.json")
            continue

        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception as e:
            print(f"[ModLoader] Ошибка чтения манифеста {mod_dir.name}: {e}")
            continue

        main_file = mod_dir / "main.py"
        if not main_file.exists():
            print(f"[ModLoader] Пропущен {mod_dir.name}: нет main.py")
            continue

        # Добавляем путь к родительской папке, чтобы мод мог импортировать core.api
        parent_path = str(mods_path.parent)
        if parent_path not in sys.path:
            sys.path.insert(0, parent_path)

        spec = importlib.util.spec_from_file_location(
            f"mods_{mod_dir.name}",
            main_file
        )
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"[ModLoader] Ошибка загрузки кода мода {mod_dir.name}: {e}")
            continue

        if hasattr(module, "register"):
            try:
                from core.api import register_command, print_success, print_info
                module.register(register_command, print_success, print_info)
            except Exception as e:
                print(f"[ModLoader] Ошибка регистрации мода {mod_dir.name}: {e}")
                continue

        loaded.append(manifest)
        print(f"[ModLoader] [+] Загружен мод: {manifest.get('name', mod_dir.name)} v{manifest.get('version', '?')}")

    return loaded
