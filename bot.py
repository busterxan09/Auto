import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReactionTypeEmoji

# Barcha botlaringizning tokenlari ro'yxati:
TOKENS = [
    "8841360251:AAHeVgnW8C7p8cYVZBgcIQWK5y20BBjMHYk",
    "8827183894:AAFHaZShqFaRFkZU92iEwlWHTFpOHhLe0NA",
    "8518942139:AAH_ogn6a5M5SMaSv-J67fn4-U_VELjDzok",
    "8901459374:AAGwK2QVsS96_V7-hbIM3CF0bPgu1v2u27I",
]

# Botlar tasodifiy tanlab qo'yadigan emojilar ro'yxati:
REACTIONS = ["❤️", "🔥", "👍", "😍"]

logging.basicConfig(level=logging.INFO)


async def start_bot(token: str):
    bot = Bot(token=token)
    dp = Dispatcher()

    @dp.channel_post()
    async def auto_react_to_channel_post(message: types.Message):
        try:
            # Telegram cheklovi sababli har bir bot 1 ta tasodifiy emoji qo'yadi
            chosen_emoji = random.choice(REACTIONS)

            await bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[ReactionTypeEmoji(emoji=chosen_emoji)],
                is_big=False,
            )
            logging.info(
                f"Reaksiya ({chosen_emoji}) qo'yildi | Bot ID: {token[:10]}..."
            )
        except Exception as e:
            logging.error(f"Xatolik yuz berdi ({token[:10]}...): {e}")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        me = await bot.get_me()
        logging.info(f"Bot muvaffaqiyatli ishga tushdi: @{me.username}")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Botni ishga tushirishda xatolik ({token[:10]}...): {e}")


async def main():
    # Barcha 4 ta botni bir vaqtda parallel ishga tushirish
    tasks = [start_bot(token) for token in TOKENS]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

