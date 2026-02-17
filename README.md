# Karina Bot

Бот на Aiogram 3.1.1 с webhook для Railway.

## Локальный запуск

1. Создай виртуальное окружение:
    python -m venv venv
    venv\Scripts\activate  # Windows

2. Установи зависимости:
    pip install -r requirements.txt

3. Создай `.env` на основе `.env.example` и вставь свой BOT_TOKEN

4. Запусти бота:
    python bot.py

## Деплой на Railway

1. Подключи репозиторий к Railway.
2. В Environments → Variables добавь:
    BOT_TOKEN
    WEBHOOK_URL
3. Deploy проекта. Бот будет онлайн.
