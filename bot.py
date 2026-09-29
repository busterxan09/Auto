import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReactionTypeEmoji

# Список всех 10 токенов:
TOKENS = [
    "8841360251:AAHeVgnW8C7p8cYVZBgcIQWK5y20BBjMHYk",
    "8827183894:AAFHaZShqFaRFkZU92iEwlWHTFpOHhLe0NA",
    "8518942139:AAH_ogn6a5M5SMaSv-J67fn4-U_VELjDzok",
    "8901459374:AAGwK2QVsS96_V7-hbIM3CF0bPgu1v2u27I",
    "8969735951:AAE8opS3yf7HqKKT41VJYe-wgj_ifsu0apE",
    "8752915627:AAFdwkzXKDlRbaqz5WRdQYuYPsAanLZ4ZeE",
    "8711233720:AAHB7ybdObUp4Jyvx1nugu4mkfvgPlgYhYQ",
    "8541715719:AAGsO2TxnCrcP5EuZXqzWwvCz6Bsk8GT-ms",
    "8763999740:AAGAGsXighP53b-RyBS3kyz5LTjhxblUr_I",
    "8908759051:AAFlkrXBmX9DPfqMgLYwVM6Z7qKWdd0vZts",
]

# Обновленный список реакций (без 👍,ggg 🎉 и 🤯):
REACTIONS = [
    "❤️",
    "🔥",
    "😍",
    "👏",
    "💯",
    "🤩",
    "🫡",
    "🚀",
    "🥰",
]

logging.basicConfig(level=logging.INFO)


async def start_bot(token: str):
    bot = Bot(token=token)
    dp = Dispatcher()

    @dp.channel_post()
    async def auto_react_to_channel_post(message: types.Message):
        try:
            chosen_emoji = random.choice(REACTIONS)

            await bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[ReactionTypeEmoji(emoji=chosen_emoji)],
                is_big=False,
            )
            logging.info(
                f"Реакция ({chosen_emoji}) поставлена | Bot ID: {token[:10]}..."
            )
        except Exception as e:
            logging.error(f"Ошибка ({token[:10]}...): {e}")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        me = await bot.get_me()
        logging.info(f"Бот запущен: @{me.username}")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка запуска бота ({token[:10]}...): {e}")


async def main():
    # Параллельный запуск 10 ботов
    tasks = [start_bot(token) for token in TOKENS]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
