import time
import random
import telebot

# 1-bot chiqarib tashlandi, endi 9 ta bot qoldi:
TOKENS = [
    "8827183894:AAEhPJdrjavzfAAYiqs3nre4To5Uj3OZO_M",  # Endi ushbu bot asosiy kuzatuvchi
    "8969735951:AAFyhvumyXv03gvw1o4r4U_47NVTeYnQOiI",
    "8841360251:AAFK8jWz2n5hKYCHuMCwyNjKP8I-_CMSorg",
    "8901459374:AAHrOyvDaURbeJrjR_QD6KqjsplBYbF939w",
    "8752915627:AAF6i0I5QpQ5SpUpvQfVZMBDaz_7bzOTDLs",
    "8711233720:AAGcVlIgiB1jGzi9R41adumyN6cbd1CllPU",
    "8908759051:AAH_rhdUcfLs-lA2jDJaCLpQHbYxQR11W3A",
    "8541715719:AAGNhI-MPy5u2a0QRY7pB4MuPdvCG2pSVdw",
    "8763999740:AAFdmBhIW0gexoqibkHFznANw2ZuEoAFbew",
]

REACTIONS = ["👍", "❤️", "🔥", "🥰", "👏", "😁", "🤩", "🚀"]

# 9 ta bot obyektini yaratamiz
bot_instances = [telebot.TeleBot(token, threaded=False) for token in TOKENS]

# Ro'yxatdagi birinchi bot (sobiq 2-bot) yangi postlarni eshitadi
main_bot = bot_instances[0]

@main_bot.channel_post_handler(func=lambda msg: True)
def handle_channel_post(message):
    print(f"\n[YANGI POST] ID: {message.message_id}")
    
    # Barcha 9 ta bot reaksiya bildiradi
    for i, bot_obj in enumerate(bot_instances, start=1):
        try:
            chosen_emoji = random.choice(REACTIONS)
            bot_obj.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(chosen_emoji)]
            )
            print(f"--> [{i}/9] Reaksiya qo'yildi: {chosen_emoji}")
            time.sleep(0.3)
        except Exception as e:
            print(f"--> [{i}/9] Xatolik: {e}")

if __name__ == "__main__":
    time.sleep(3)

    for b in bot_instances:
        try:
            b.remove_webhook()
        except Exception:
            pass

    print("Barcha 9 ta bot tayyor. Kanal kuzatish boshlandi...")

    while True:
        try:
            main_bot.infinity_polling(timeout=30, long_polling_timeout=10, skip_pending=True)
        except Exception as e:
            print(f"Ulanish uzildi, qayta tiklanmoqda: {e}")
            time.sleep(5)
