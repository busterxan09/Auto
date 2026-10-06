import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Har bir bot va unga biriktirilgan alohida reaksiya
BOT_REACTIONS = [
    {"token": "8873673862:AAHkh6-SnfK7MGqr7xuEegxcBE0jlvCiJQE", "emoji": "👍"},
    {"token": "8957810259:AAGDbR19Q-6LCFL_dGEhH9gnLD3an0ndnF0", "emoji": "❤️"},
    {"token": "8752915627:AAFDAZr3qpUy8t8mJJ06n16A8pO1dj5Yf1Y", "emoji": "🔥"},
    {"token": "8969735951:AAGwKdLEZScmFLnrXGLTF5JRg7MSqyl6ZIo", "emoji": "🎉"},
    {"token": "8901459374:AAHGwg-O7p2UjUwBqJULBCYU9AaWW7UEQ_Q", "emoji": "🤩"},
    {"token": "8518942139:AAHQULBQKS0UCYxN66W81JJxNo6xEXyg1Wo", "emoji": "👏"},
    {"token": "8841360251:AAEnDzoJ_CsxukrzfNle-QxMMLahvJPn0-U", "emoji": "⚡"},
    {"token": "8711233720:AAH-uIaTKo7aW2m0XLoZSFeebdJe7H0HYec", "emoji": "🏆"},
    {"token": "8541715719:AAFGNDRIEn0cwgvjUBlHMSOAWpknfc00PMI", "emoji": "💯"},
    {"token": "8908759051:AAEvxSu2UfULGryrIp5s9CJRWl3bvNZIPG4", "emoji": "🫡"},
    {"token": "8763999740:AAHYKvyfv1ypC5rDZ_F9VulFa9GMqJauYZw", "emoji": "😍"}
]


# Kanalga yangi post tushganda ishlaydigan funksiya
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    if not post:
        return

    chat_id = post.chat_id
    message_id = post.message_id
    assigned_emoji = context.bot_data.get("emoji", "👍")

    try:
        await context.bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=[{"type": "emoji", "emoji": assigned_emoji}]
        )
        print(f"[{assigned_emoji}] Reaksiya bosildi -> Post ID: {message_id}")
    except Exception as e:
        print(f"Xatolik: {e}")


async def start_bot(bot_info):
    token = bot_info["token"]
    emoji = bot_info["emoji"]

    app = ApplicationBuilder().token(token).build()
    app.bot_data["emoji"] = emoji

    # Kanaldagi postlarni ushlash uchun handler
    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, handle_channel_post))

    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)


async def main():
    print("Barcha botlar Railway'da ishga tushdi va kanalni kuzatmoqda...")
    # Barcha botlarni parallel ravishda tinglash rejimiga o'tkazish
    tasks = [start_bot(b) for b in BOT_REACTIONS]
    await asyncio.gather(*tasks)

    # Server to'xtab qolmasligi uchun doimiy sikl
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
