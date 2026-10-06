import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReactionTypeEmoji
from aiogram.exceptions import TelegramUnauthorizedError

TOKENS = [
    "8841360251:AAHeVgnW8C7p8cYVZBgcIQWK5y20BBjMHYk",
    "8827183894:AAFHaZShqFaRFkZU92iEwlWHTFpOHhLe0NA",
    "8518942139:AAH_ogn6a5M5SMaSv-J67fn4-U_VELjDzok",
    "8901459374:AAGwK2QVsS96_V7-hbIM3CF0bPgu1v2u27I",
    "8969735951:AAE8opS3yf7HqKKT41VJYe-wgj_ifsu0apE",
    "8752915627:AAFdwkzXKDlRbaqz5WRdQYuYPsAanLZ4ZeE",
    "8711233720:AAHB7ybdObUp4Jyvx1nugu4mkfvgPlgYhYQ",
    "8541715719:AAGsO2TxnCrcP5EuZXqzWwvCz6Bsk8GT-ms",
]

REACTIONS = ["🔥", "❤️", "💯", "🕊️"]

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
            logging.error(f"Ошибка реакции ({token[:10]}...): {e}")

    try:
        # Проверяем токен перед запуском
        me = await bot.get_me()
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info(f"Бот запущен успешно: @{me.username}")
        await dp.start_polling(bot)
    except TelegramUnauthorizedError:
        logging.error(
            f"НЕВЕРНЫЙ ТОКЕН! Пропущен: {token[:10]}... Проверьте токен в @BotFather!"
        )
    except Exception as e:
        logging.error(f"Ошибка запуска бота ({token[:10]}...): {e}")
    finally:
        await bot.session.close()


async def main():
    tasks = [start_bot(token) for token in TOKENS]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
