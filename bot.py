import os
import random
from flask import Flask, request
import telebot

app = Flask(__name__)

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

# Botlarni yaratish
bots = {token.split(":")[0]: telebot.TeleBot(token) for token in TOKENS}

# Sizning aniq domeningiz:
WEBHOOK_URL_BASE = "https://worker-production-755e.up.railway.app"

@app.route("/", methods=["GET", "HEAD"])
def index():
    return "OK", 200

@app.route("/webhook/<bot_id>", methods=["POST"])
def webhook(bot_id):
    if bot_id in bots:
        bot = bots[bot_id]
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        
        if update and update.channel_post:
            msg = update.channel_post
            try:
                chosen_emoji = random.choice(REACTIONS)
                bot.set_message_reaction(
                    chat_id=msg.chat.id,
                    message_id=msg.message_id,
                    reaction=[telebot.types.ReactionTypeEmoji(chosen_emoji)]
                )
                print(f"Reaksiya ({chosen_emoji}) qo'yildi | Bot ID: {bot_id}")
            except Exception as e:
                print(f"Reaksiya qo'yishda xatolik: {e}")
                
    return "OK", 200

def setup_webhooks():
    for token in TOKENS:
        bot_id = token.split(":")[0]
        webhook_url = f"{WEBHOOK_URL_BASE}/webhook/{bot_id}"
        bot = bots[bot_id]
        try:
            bot.remove_webhook()
            bot.set_webhook(url=webhook_url)
            print(f"Webhook o'rnatildi: {bot_id}")
        except Exception as e:
            print(f"Webhook xatosi ({bot_id}): {e}")

if __name__ == "__main__":
    setup_webhooks()
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
