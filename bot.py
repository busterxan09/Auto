import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReactionTypeEmoji

# 8 adet bot jetonunuz
TOKENS = [
    "8957810259:AAHdXldV9mFjcxFSw5OwtLaZ1YWkUWnj00I",  # Master Bot (Dinleyici)
    "8752915627:AAEYf-0dfIaJ1bC25uRaKwA8KdA-s5lEE0o",
    "8901459374:AAHFxk4ocr5h7dgIeOzfRZJk2ORNHQC5MI4",
    "8841360251:AAHBBSuiOEaZhQOVVEym51uUm6ZxQz4cDWE",
    "8873673862:AAFJs0xdcPHkCNIRl564_6aEvkL7i697u4g",
    "8969735951:AAGvy357HEpeFp4okziwIfKmH3adzKwJ6XY",
    "8518942139:AAFoxkfcyFrJzFHz_JS2RtRBlvehj1XktLY",
    "8711233720:AAFhYEpOwPCgscduOe1M_lStND404N3sMig",
]

# Belirlenen 4 reaksiyon
REACTIONS = ["🔥", "❤️", "💯", "🕊️"]

logging.basicConfig(level=logging.INFO)

# Tüm bot nesnelerini oluşturuyoruz
bots = [Bot(token=t.strip()) for t in TOKENS]
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
        logging.info(f"Reaksiyon eklendi ({chosen_emoji})")
    except Exception as e:
        logging.error(f"Reaksiyon ekleme hatası: {e}")

@dp.channel_post()
async def auto_react_to_channel_post(message: types.Message):
    logging.info(f"Yeni kanal gönderisi tespit edildi! Message ID: {message.message_id}")
    # Tüm 8 bot aynı anda paralel olarak reaksiyon bırakır
    tasks = [send_reaction_safe(b, message.chat.id, message.message_id) for b in bots]
    await asyncio.gather(*tasks)

async def main():
    # Çakışmaları önlemek için eski webhook'ları temizliyoruz
    for b in bots:
        try:
            await b.delete_webhook(drop_pending_updates=True)
        except Exception:
            pass

    logging.info("Master Bot dinleme modunda başlatıldı...")
    # SADECE İLK BOT (bots[0]) POLLING YAPAR - ÇAKIŞMA TAMAMEN ÖNLENİR
    await dp.start_polling(bots[0])

if __name__ == "__main__":
    asyncio.run(main())
