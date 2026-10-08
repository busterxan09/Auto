import asyncio
import logging
import os
import random
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReactionTypeEmoji

# Загружаем переменные окружения
load_dotenv()

# Получаем токены из переменной BOT_TOKENS
raw_tokens = os.getenv("BOT_TOKENS", "")
TOKENS = [t.strip() for t in raw_tokens.split(",") if t.strip()]

if not TOKENS:
    raise ValueError("BOT_TOKENS не найдены! Проверьте вкладку Variables в Railway.")

# Определенные реакции
REACTIONS = ["🔥", "❤️", "💯", "🕊️"]

logging.basicConfig(level=logging.INFO)

# Создаем объекты всех ботов
bots = [Bot(token=t) for t in TOKENS]
dp = Dispatcher()

async def send_reaction_safe(bot: Bot, chat_id: int, message_id: int):
    try:
        chosen_emoji = random.choice(REACTIONS)
        await bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=[ReactionTypeEmoji(emoji=chosen_emoji)],
            is_big=False
        )
        logging.info(f"Реакция добавлена ({chosen_emoji})")
    except Exception as e:
        logging.error(f"Ошибка добавления реакции: {e}")

@dp.channel_post()
async def auto_react_to_channel_post(message: types.Message):
    logging.info(f"Обнаружен новый пост в канале! Message ID: {message.message_id}")
    # Все боты одновременно оставляют реакцию
    tasks = [send_reaction_safe(b, message.chat.id, message.message_id) for b in bots]
    await asyncio.gather(*tasks)

async def main():
    # Очищаем старые вебхуки
    for b in bots:
        try:
            await b.delete_webhook(drop_pending_updates=True)
        except Exception:
            pass

    logging.info("Master Bot запущен в режиме прослушивания...")
    # Полллинг делает только первый бот для исключения конфликтов
    await dp.start_polling(bots[0])

if __name__ == "__main__":
    asyncio.run(main())
