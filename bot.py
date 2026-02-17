import asyncio
import logging
import random
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from dotenv import load_dotenv

load_dotenv()  # загружаем .env локально

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

if not BOT_TOKEN or not WEBHOOK_URL:
    raise ValueError("BOT_TOKEN или WEBHOOK_URL не найдены в переменных окружения!")

WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

MEDIA_FOLDER = "media"


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Приветики всем! Я Кариночка 💋")


@dp.message()
async def trigger_handler(message: types.Message):
    # Ответ на сообщение бота
    if message.reply_to_message:
        if message.reply_to_message.from_user.id == (await bot.me()).id:
            await message.answer("Ой, что такое?)")
            return

    # Если тегнули бота
    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                mention = message.text[entity.offset:entity.offset + entity.length]
                if mention.lower() == "@radonkarina_bot":
                    await message.answer("Ой, что такое?)")
                    return

    if not message.text:
        return

    text = message.text.lower()

    if "лярва" in text:
        try:
            media_files = [
                f for f in os.listdir(MEDIA_FOLDER)
                if f.endswith((".jpg", ".png", ".gif", ".mp4", ".webm"))
            ]

            if not media_files:
                return

            random_file = random.choice(media_files)
            file_path = os.path.join(MEDIA_FOLDER, random_file)
            file = FSInputFile(file_path)

            if random_file.endswith((".jpg", ".png")):
                await message.answer_photo(file)
            elif random_file.endswith(".gif"):
                await message.answer_animation(file)
            elif random_file.endswith(".mp4"):
                await message.answer_video(file)
            elif random_file.endswith(".webm"):
                await message.answer_document(file)

        except Exception as e:
            logging.error(e)


async def main():
    PORT = int(os.environ.get("PORT", 8080))
    logging.info(f"Webhook установлен на {WEBHOOK_URL}{WEBHOOK_PATH}")

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(url=f"{WEBHOOK_URL}{WEBHOOK_PATH}")

    # Запуск webhook сервера (Aiogram 3.3+)
    from aiohttp import web

    async def handle(request):
        update = types.Update(**await request.json())
        await dp.process_update(update)
        return web.Response(text="OK")

    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logging.info(f"Webhook слушает на порту {PORT}")

    while True:
        await asyncio.sleep(3600)  # держим сервер живым


if __name__ == "__main__":
    asyncio.run(main())
