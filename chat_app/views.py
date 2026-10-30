from __future__ import annotations

import json
import random
from random import choice

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .config import ACTIVE_VARIANT

# ---------------------------------------------------------------------------
# Единственный метод API активного чата:
#   POST /api/chat/send/
#   body: {"message": "текст пользователя"}
#   response 200: {"reply": "ответное сообщение"}
#   response 400: {"error": "описание ошибки"}
#
# Демо-робот «Робот-Учёный» (доступен при каждом запуске):
#   страница  — GET /demo/
#   метод API — POST /api/chat/send_demo/
#   логика    — build_reply_demo (перенесена без изменений, суффикс _demo)
# ---------------------------------------------------------------------------


def _parse_message(request):
    """Разбирает JSON-тело запроса. Возвращает (message, error_response)."""
    try:
        data = json.loads(request.body or b'{}')
    except json.JSONDecodeError:
        error = JsonResponse(
            {'error': 'Тело запроса должно быть валидным JSON'}, status=400
        )
        return None, error

    message = str(data.get('message') or '').strip()
    if not message:
        error = JsonResponse({'error': 'Сообщение не может быть пустым'}, status=400)
        return None, error
    return message, None


# ===========================================================================
# ДЕМО: «Робот-Учёный» (логика НЕ менялась, переименована с суффиксом _demo)
# ===========================================================================
def build_reply_demo(message: str) -> str:
    """Формирует ответное сообщение бота (учебная демо-заглушка)."""
    text = message.strip().lower()

    greetings = ('привет', 'здравствуй', 'добрый день', 'hello', 'hi', 'салют')
    if any(word in text for word in greetings):
        return (
            'Привет-привет! 👋 Я Робот-Учёный, твой учебный напарник. '
            'Спрашивай про математику, науку, космос или динозавров — '
            'скучно не будет! 🚀'
        )

    if any(word in text for word in ('пример', 'задач', 'матем', 'сложить', 'умнож')):
        return (
            'Математика — это весело! 🧮 Вот тебе хитрость: 12 × 12 = 144, '
            '15 × 15 = 225, а 25 × 25 = 625. Заметил(а) закономерность? '
            'Это «квадраты чисел»! Попроси меня придумать тебе пример посложнее. 😉'
        )

    if 'динозавр' in text:
        return (
            'Динозавры — супертема! 🦖 Тираннозавр весил как 4 современные машины, '
            'а самый маленький динозаврик был размером с курицу! Хочешь узнать, '
            'почему они вымерли? Задай вопрос «Почему вымерли динозавры?» 🌋'
        )

    if any(word in text for word in ('физик', 'гравит', 'сила тяжест', 'небо голуб', 'молн')):
        return (
            'Отличный научный вопрос! ✨ Знаешь, почему небо голубое? '
            'Солнечный свет состоит из всех цветов, а голубой рассеивается '
            'в атмосфере лучше всех — поэтому мы видим именно его! Попробуй '
            'представить атмосферу как гигантское голубое светоотражающее зеркало. 🌈'
        )

    if any(word in text for word in ('космос', 'планет', 'звезд', 'лун')):
        return (
            'Космос — бесконечное приключение! 🪐 Если бы ты прыгнул(а) на Луне, '
            'то взлетел(а) бы в 6 раз выше, чем на Земле. А на Юпитере один день '
            'длится всего 10 часов! Узнать что-нибудь ещё о планетах? 🌍'
        )

    if any(word in text for word in ('?', 'как', 'почему', 'что', 'когда', 'где')):
        return (
            'Интересный вопрос! 🧠 Сначала подумай сам(а): что ты уже знаешь об '
            'этом? Потом мы проверим твою гипотезу вместе — учёные именно так и '
            'делают! 🔬 Расскажи, что думаешь?'
        )

    return random.choice([
        'Я тебя понял(а)! 😄 А теперь попробуй превратить эту мысль в вопрос — '
        'например, «Почему...?» или «Как это работает?». Так учёные добывают знания!',
        'Ого, интересная мысль! ✨ Давай заглянем в «копилку знаний»: о чём бы '
        'ты хотел(а) узнать подробнее — математика, природа или космос?',
        'Супер! 🎉 За такой настрой тебе +25 XP! А знаешь ли ты, что любое '
        'явление можно проверить экспериментом? Попроси меня помочь придумать опыт!',
        'Круто! 🤩 Я записал(а) это в свою «таблицу знаний». Задавай следующий '
        'вопрос — мы вместе разберёмся в чём угодно!',
    ])


# ===========================================================================
# НОВЫЕ ВАРИАНТЫ ОФОРМЛЕНИЯ
# build_reply_* оставлены заглушкой «ПРИВЕТ» — код внутри НЕ реализован.
# ===========================================================================
def build_reply_magic(message: str) -> str:
    # TODO(магический помощник): волшебник в академии магии — задания,
    # загадки, проверка ответов, очки опыта и уровни.
    text = message.strip().lower()
    greetings = ('привет', 'здравствуй', 'добрый день', 'hello', 'hi', 'салют')
    greetings_bot = ['Приветствую тебя в нашей академии магии и колдовства',
                     "Приветсвую тебя, молодой маг",
                     "Готов к изучению магии? Ну что же, начнём!"
                     ]
    if any(word in text for word in greetings):
        return random.choice(greetings_bot)
    # Принт для дебага
    print(text)
    return 'ПРИВЕТ'


def build_reply_ship(message: str) -> str:
    # TODO(бортовой компьютер): состояние корабля, двигатели, топливо,
    # исследование планет, случайные события, аварии.
    text = message.strip().lower()
    greetings = ('привет', 'здравствуй', 'добрый день', 'hello', 'hi', 'салют')
    greetings_bot = ['Здравствуйте сэр', 'Добрый вечер капитан' , 'Здравствуйте']
    if any(word in text for word in greetings):
        return random.choice(greetings_bot)
    # Принт для дебага
    print(text)
    return 'ПРИВЕТ'

def build_reply_detective(message: str) -> str:
    # TODO(детективный бот): описание дела, улики, допрос свидетелей,
    # проверка версий пользователя, результат расследования.

    text = message.strip().lower()
    greetings = ('привет', 'здравствуй', 'добрый день', 'hello', 'hi', 'салют')
    greetings_bot = ['ну где там наш детектив? Вот он!', 'салют детектив']
    if any(word in text for word in greetings):
        return random.choice(greetings_bot)
    # Принт для дебага
    print(text)
    return 'ПРИВЕТ'


def build_reply_trader(message: str) -> str:
    # TODO(умный торговец): ассортимент и цены, покупка/продажа,
    # баланс игрока, случайные скидки, подсчёт покупки.
    return 'ПРИВЕТ'


def build_reply_survival(message: str) -> str:
    text = message.strip().lower()

    greetings = ('привет', 'здравствуй', 'добрый день', 'hello', 'hi', 'салют')
    greetings_bot = [" добро пожаловать на курсы по выживанию","здравствуй новичок это курсы по выживанию"]
    if any(word in text for word in greetings):
        return random.choice(greetings_bot)
    # Принт для дебага
    print(text)
    return 'ПРИВЕТ'


def build_reply_dungeon(message: str) -> str:
    # TODO(хранитель подземелья): генерация комнат и событий, сражение/
    # исследование/отдых, здоровье и инвентарь, награды, память приключения.

    text = message.strip().lower()
    greetings = ('привет', 'здравствуй', 'добрый день', 'hello', 'hi', 'салют')
    greetings_bot = ['привет', 'здравствуй', 'здравия желаю', 'приветствую', 'здравствуйте']
    if any(word in text for word in greetings):
        return choice(greetings_bot)
    # Принт для дебага
    print(text)
    return 'ПРИВЕТ'


# Диспетчер: активный вариант (config.json) -> его build_reply_*
REPLY_BUILDERS = {
    'robot': build_reply_demo,
    'magic': build_reply_magic,
    'ship': build_reply_ship,
    'detective': build_reply_detective,
    'trader': build_reply_trader,
    'survival': build_reply_survival,
    'dungeon': build_reply_dungeon,
}


def chat_page(request):
    """Страница активного (настроенного в config.json) варианта чата."""
    return render(request, f'chat/{ACTIVE_VARIANT}.html')


def chat_page_demo(request):
    """Демо-страница «Робот-Учёный», доступна всегда по /demo/."""
    return render(request, 'chat/robot.html')


@require_POST
def api_chat_send(request):
    """POST /api/chat/send/ — метод активного варианта чата."""
    message, error = _parse_message(request)
    if error:
        return error
    builder = REPLY_BUILDERS.get(ACTIVE_VARIANT, build_reply_demo)
    return JsonResponse({'reply': builder(message)})


@require_POST
def api_chat_send_demo(request):
    """POST /api/chat/send_demo/ — метод демо-робота (всегда один и тот же)."""
    message, error = _parse_message(request)
    if error:
        return error
    return JsonResponse({'reply': build_reply_demo(message)})