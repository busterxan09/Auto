import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReactionTypeEmoji

# Yangilangan 10 ta bot tokenlari:
TOKENS = [
    "8518942139:AAFSbCQ7QR3q5bBZIa7M9lVJTk23L7N7KrA",
    "8827183894:AAEhPJdrjavzfAAYiqs3nre4To5Uj3OZO_M",
    "8969735951:AAFyhvumyXv03gvw1o4r4U_47NVTeYnQOiI",
    "8841360251:AAFK8jWz2n5hKYCHuMCwyNjKP8I-_CMSorg",
    "8901459374:AAHrOyvDaURbeJrjR_QD6KqjsplBYbF939w",
    "8752915627:AAF6i0I5QpQ5SpUpvQfVZMBDaz_7bzOTDLs",
    "8711233720:AAGcVlIgiB1jGzi9R41adumyN6cbd1CllPU",
    "8908759051:AAH_rhdUcfLs-lA2jDJaCLpQHbYxQR11W3A",
    "8541715719:AAGNhI-MPy5u2a0QRY7pB4MuPdvCG2pSVdw",
    "8763999740:AAFdmBhIW0gexoqibkHFznANw2ZuEoAFbew",
]

# Tanlangan reaksiyalar ro'yxati:
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
                f"Reaksiya ({chosen_emoji}) qo'yildi | Bot ID: {token[:10]}..."
            )
        except Exception as e:
            logging.error(f"Xatolik yuz berdi ({token[:10]}...): {e}")

    while True:
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            me = await bot.get_me()
            logging.info(f"Bot muvaffaqiyatli ishga tushdi: @{me.username}")

            await dp.start_polling(
                bot, allowed_updates=["channel_post"], handle_signals=False
            )
            break
        except Exception as e:
            logging.error(
                f"Ulanishda xatolik ({token[:10]}...): {e}. 10 soniyadan so'ng qayta ulanadi..."
            )
            await asyncio.sleep(10)


async def main():
    tasks = [start_bot(token) for token in TOKENS]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

