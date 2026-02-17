import asyncio
import logging
import random
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

logging.basicConfig(level=logging.INFO)

# Берем токен из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Приветики всем, я Кариночка 💋")


@dp.message()
async def trigger_handler(message: types.Message):
    # Если ответ на сообщение бота
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


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
