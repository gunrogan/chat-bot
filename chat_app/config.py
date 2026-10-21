"""Конфигурация активного варианта оформления чата.

Вариант задаётся в файле config.json (корень проекта) и читается
ОДИН РАЗ при запуске приложения::

    {
        "variant": "magic"
    }

Допустимые значения variant:
    robot, magic, ship, detective, trader, survival, dungeon

Робот-Учёный («demo») не зависит от конфигурации и всегда доступен
на отдельном пути /demo/.
"""

import json
from pathlib import Path

# Корень проекта (там же лежит config.json)
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / 'config.json'

VALID_VARIANTS = (
    'robot',      # Робот-Учёный (демо-вариант)
    'magic',      # Магический помощник
    'ship',       # Бортовой компьютер космического корабля
    'detective',  # Детективный бот
    'trader',     # Умный торговец
    'survival',   # Бот выживания
    'dungeon',    # Хранитель подземелья
)

DEFAULT_VARIANT = 'magic'


def load_variant() -> str:
    """Возвращает активный вариант из config.json (или значение по умолчанию)."""
    try:
        with open(CONFIG_PATH, encoding='utf-8') as file:
            data = json.load(file)
        variant = str(data.get('variant', '')).strip().lower()
        if variant in VALID_VARIANTS:
            return variant
    except (OSError, ValueError, TypeError):
        pass  # нет файла / битый JSON / неверное значение -> значение по умолчанию
    return DEFAULT_VARIANT


# Активный вариант, определяется при импорте модуля (т.е. при запуске Django).
ACTIVE_VARIANT = load_variant()