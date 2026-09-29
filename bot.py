import telebot
import random
import time
from threading import Thread

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

REACTIONS = ["❤️️", "🔥", "😍", "👏", "💯", "🤩", "🫡", "🚀", "🥰"]

def run_bot(token):
    bot = telebot.TeleBot(token)

    @bot.channel_post_handler(func=lambda message: True)
    def handle_post(message):
        try:
            chosen_emoji = random.choice(REACTIONS)
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(chosen_emoji)]
            )
            print(f"Reaksiya ({chosen_emoji}) qo'yildi | Bot: {token[:10]}...")
        except Exception as e:
            print(f"Xatolik ({token[:10]}...): {e}")

    # Webhook bo'lsa o'chiramiz
    bot.remove_webhook()
    print(f"Bot muvaffaqiyatli ishga tushdi: {token[:10]}...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    threads = []
    for token in TOKENS:
        t = Thread(target=run_bot, args=(token,))
        t.start()
        threads.append(t)
        time.sleep(1)  # Botlarni 1 soniyalik pauza bilan yoqish

    for t in threads:
        t.join()
