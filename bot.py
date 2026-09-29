import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReactionTypeEmoji

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

REACTIONS = ["❤️", "🔥", "😍", "👏", "💯", "🤩", "🫡", "🚀", "🥰"]

logging.basicConfig(level=logging.INFO)


async def run_single_bot(token: str):
    bot = Bot(token=token)
    dp = Dispatcher()

    @dp.channel_post()
    async def auto_react(message: types.Message):
        try:
            chosen_emoji = random.choice(REACTIONS)
            await bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[ReactionTypeEmoji(emoji=chosen_emoji)],
                is_big=False,
            )
            logging.info(f"Reaksiya qo'yildi ({chosen_emoji}) | Bot: {token[:10]}...")
        except Exception as e:
            logging.error(f"Xatolik ({token[:10]}...): {e}")

    # Webhook'ni tozalab, Telegram bilan ulanishni barqarorlashtiramiz
    while True:
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            me = await bot.get_me()
            logging.info(f"Bot muvaffaqiyatli ulandi: @{me.username}")
            
            # Polling'ni ziddiyatlarsiz yurgazish
            await dp.start_polling(
                bot, 
                allowed_updates=["channel_post"], 
                handle_signals=False
            )
            break
        except Exception as e:
            logging.warning(f"Sessiya almashinmoqda ({token[:10]}...): 5 soniya kutilmoqda...")
            await asyncio.sleep(5)


async def main():
    # Botlarni Telegram serveriga bosim o'tkazmasdan 2 soniyalik interval bilan ketma-ket ulash
    tasks = []
    for token in TOKENS:
        task = asyncio.create_task(run_single_bot(token))
        tasks.append(task)
        await asyncio.sleep(2)  # Har bir bot orasida 2 soniya pauza

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
