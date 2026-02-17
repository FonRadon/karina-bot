import os
import logging
import random
from aiohttp import web

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# Подгружаем .env для локальной разработки
load_dotenv()

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")

WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # URL, который даст Railway, например: https://имя-проекта.up.railway.app

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Обработчики ---
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Приветики всем, я Кариночка 💋")


@dp.message()
async def trigger_handler(message: types.Message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.id == (await bot.me()).id:
            await message.answer("Ой, что такое?)")
            return

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
                f for f in os.listdir("media")
                if f.endswith((".jpg", ".png", ".gif", ".mp4", ".webm"))
            ]
            if not media_files:
                return

            random_file = random.choice(media_files)
            file_path = os.path.join("media", random_file)
            file = types.FSInputFile(file_path)

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

# --- Aiohttp сервер для webhook ---
async def handle(request):
    data = await request.json()
    update = types.Update(**data)
    await dp.process_update(update)
    return web.Response(text="OK")

app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle)

async def on_startup():
    await bot.delete_webhook()
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")
    logging.info(f"Webhook установлен на {WEBHOOK_URL}{WEBHOOK_PATH}")

async def on_cleanup(app):
    await bot.delete_webhook()
    await bot.session.close()

app.on_startup.append(lambda app: on_startup())
app.on_cleanup.append(lambda app: on_cleanup(app))

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
