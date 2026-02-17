import os
import random
import logging
from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, MessageEntity
from aiogram.enums import ParseMode
import asyncio

# Загружаем переменные окружения
load_dotenv()

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")

# Путь к папке с медиафайлами
MEDIA_FOLDER = Path("media")

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция для получения случайного файла из папки media
def get_random_media_file():
    """Возвращает случайный файл из папки media"""
    try:
        # Получаем все файлы из папки media
        files = [f for f in MEDIA_FOLDER.iterdir() if f.is_file()]
        
        if not files:
            return None
        
        # Выбираем случайный файл
        random_file = random.choice(files)
        return random_file
    except Exception as e:
        logging.error(f"Ошибка при получении файла: {e}")
        return None

# Функция для определения типа файла
def get_media_type(file_path: Path):
    """Определяет тип медиафайла по расширению"""
    ext = file_path.suffix.lower()
    
    if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.webp']:
        return 'photo'
    elif ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
        return 'video'
    elif ext == '.gif':
        return 'animation'
    else:
        return 'unknown'

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("оу, приветики 💋")

# Обработчик команды /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "✨ *Команды бота:*\n"
        "/start - приветствие\n"
        "/help - эта справка\n\n"
        "📝 *Секретное слово:* лярва\n"
        "(Напиши его и получишь сюрприз!)",
        parse_mode=ParseMode.MARKDOWN
    )

# Обработчик ответов на сообщения бота
@dp.message(F.reply_to_message)
async def handle_reply(message: types.Message):
    # Проверяем, что отвечают на сообщение бота
    if message.reply_to_message and message.reply_to_message.from_user.id == bot.id:
        await message.reply("это я, кариночка 💋")

# Обработчик упоминания бота (тег)
@dp.message(F.text)
async def handle_mention(message: types.Message):
    # Проверяем, упомянули ли нашего бота
    if not message.entities:
        return
    
    bot_username = (await bot.get_me()).username
    
    for entity in message.entities:
        if entity.type == "mention":
            mention = message.text[entity.offset:entity.offset + entity.length]
            if mention == f"@{bot_username}":
                await message.reply("ой, что такое?")
                return

# Обработчик текстовых сообщений с проверкой на слово "лярва"
@dp.message(F.text)
async def check_larva_word(message: types.Message):
    # Проверяем, содержит ли сообщение слово "лярва" в любом регистре
    text = message.text.lower().strip()
    
    if "лярва" in text:
        # Получаем случайный файл
        random_file = get_random_media_file()
        
        if random_file:
            try:
                # Создаем объект FSInputFile для отправки
                media_file = FSInputFile(random_file)
                
                # Определяем тип файла и отправляем соответствующим методом
                media_type = get_media_type(random_file)
                
                if media_type == 'photo':
                    await message.answer_photo(
                        photo=media_file,
                        caption="🌸 Держи фоточку!"
                    )
                elif media_type == 'video':
                    await message.answer_video(
                        video=media_file,
                        caption="🎥 Держи видосик!"
                    )
                elif media_type == 'animation':  # для GIF
                    await message.answer_animation(
                        animation=media_file,
                        caption="✨ Держи гифку!"
                    )
                else:
                    # Если тип не определен, отправляем как документ
                    await message.answer_document(
                        document=media_file,
                        caption="📎 Держи файлик!"
                    )
                    
                logging.info(f"Отправлен файл: {random_file.name}")
                
            except Exception as e:
                logging.error(f"Ошибка при отправке файла {random_file}: {e}")
                await message.answer("😢 Ой, что-то пошло не так с файликом...")
        else:
            await message.answer("😢 Ой, а у меня закончились медиафайлы...")

# Запуск бота
async def main():
    logging.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())