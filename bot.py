import os
import random
import telebot
from flask import Flask, request

# Railway taqdim etgan domen (oxiridagi / belgisisiz):
WEBHOOK_URL = "https://worker-production-755e.up.railway.app"


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

app = Flask(__name__)
bots = {}

for token in TOKENS:
    bot = telebot.TeleBot(token, threaded=False)
    
    def make_handler(b):
        def handle_post(message):
            try:
                chosen_emoji = random.choice(REACTIONS)
                b.set_message_reaction(
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    reaction=[telebot.types.ReactionTypeEmoji(chosen_emoji)]
                )
                print(f"Reaksiya ({chosen_emoji}) qo'yildi | Bot: {b.token[:10]}...")
            except Exception as e:
                print(f"Xatolik: {e}")
        return handle_post

    bot.channel_post_handler(func=lambda msg: True)(make_handler(bot))
    bots[token] = bot

@app.route("/webhook/<token>", methods=["POST"])
def receive_update(token):
    if token in bots:
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bots[token].process_new_updates([update])
        return "OK", 200
    return "Forbidden", 403

def setup_webhooks():
    for token, bot in bots.items():
        webhook_path = f"{WEBHOOK_URL}/webhook/{token}"
        bot.remove_webhook()
        bot.set_webhook(url=webhook_path)
        print(f"Webhook o'rnatildi: {token[:10]}...")

if __name__ == "__main__":
    setup_webhooks()
    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)
