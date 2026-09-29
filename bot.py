import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import ReactionTypeEmoji

# Yangi bot tokeni
BOT_TOKEN = "8841360251:AAHeVgnW8C7p8cYVZBgcIQWK5y20BBjMHYk"

# Bot postga ushbu emojilardan TASODIFIY 1 TASINI qo'yadi:
REACTIONS = ["❤️", "🔥", "👍", "😍"]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("Bot faol ishlamoqda!")


@dp.channel_post()
async def auto_react_to_channel_post(message: types.Message):
    try:
        # Telegram cheklovi sababli ro'yxatdan faqat 1 ta emoji tanlanadi
        chosen_emoji = random.choice(REACTIONS)

        await bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=[ReactionTypeEmoji(emoji=chosen_emoji)],
            is_big=False,
        )
        logging.info(f"Reaksiya ({chosen_emoji}) qo'yildi: {message.message_id}")
    except Exception as e:
        logging.error(f"Reaksiya qo'yishda xatolik: {e}")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
