import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReactionTypeEmoji
from aiogram.exceptions import TelegramUnauthorizedError

# Barcha 8 ta yangilangan tokenlar ro'yxati:
TOKENS = [
    "8957810259:AAHdXldV9mFjcxFSw5OwtLaZ1YWkUWnj00I",
    "8752915627:AAEYf-0dfIaJ1bC25uRaKwA8KdA-s5lEE0o",
    "8901459374:AAHFxk4ocr5h7dgIeOzfRZJk2ORNHQC5MI4",
    "8841360251:AAHBBSuiOEaZhQOVVEym51uUm6ZxQz4cDWE",
    "8873673862:AAFJs0xdcPHkCNIRl564_6aEvkL7i697u4g",
    "8969735951:AAGvy357HEpeFp4okziwIfKmH3adzKwJ6XY",
    "8518942139:AAFoxkfcyFrJzFHz_JS2RtRBlvehj1XktLY",
    "8711233720:AAFhYEpOwPCgscduOe1M_lStND404N3sMig",
]

# Tanlangan 4 ta reaksiya:
REACTIONS = ["🔥", "❤️", "💯", "🕊️️"]

logging.basicConfig(level=logging.INFO)


async def start_bot(token: str):
    token = token.strip()
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

    try:
        me = await bot.get_me()
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info(f"MUVAFFAQIYATLI ISHGA TUSHMADI: @{me.username}")
        await dp.start_polling(bot)
    except TelegramUnauthorizedError:
        logging.error(
            f"XATO TOKEN! O'tkazib yuborildi: {token[:10]}... @BotFather'dan tekshiring!"
        )
    except Exception as e:
        logging.error(f"Botni ishga tushirishda xatolik ({token[:10]}...): {e}")
    finally:
        await bot.session.close()


async def main():
    tasks = [start_bot(token) for token in TOKENS]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.rund(main())
