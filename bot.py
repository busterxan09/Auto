import time
import random
import telebot

# 10 ta bot tokenlari
TOKENS = [
    "8518942139:AAFSbCQ7QR3q5bBZIa7M9lVJTk23L7N7KrA",  # Asosiy kuzatuvchi bot
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

REACTIONS = ["👍", "❤️", "🔥", "🥰", "👏", "😁", "🤩", "🫡", "🚀", "🎉"]

# Barcha bot obyektlarini yaratib olamiz
bot_instances = [telebot.TeleBot(token) for token in TOKENS]

# Faqat 1-bot kanaldagi yangi postlarni eshitadi (Conflict 409 xatosi umuman bo'lmaydi!)
main_bot = bot_instances[0]

# Har bir botdan keladigan webhooklarni tozalaymiz
for b in bot_instances:
    try:
        b.remove_webhook()
    except Exception:
        pass

print("Barcha botlar tayyorlandi. Kanal kuzatilmoqda...")

@main_bot.channel_post_handler(func=lambda msg: True)
def handle_channel_post(message):
    print(f"\n[YANGI POST DETEKT QILINDI] ID: {message.message_id}")
    
    # 10 ta botning har biri navbat bilan reaksiya bosadi
    for i, bot_obj in enumerate(bot_instances, start=1):
        try:
            chosen_emoji = random.choice(REACTIONS)
            bot_obj.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(chosen_emoji)]
            )
            print(f"--> [{i}/10] Bot reaksiya qo'ydi: {chosen_emoji}")
            time.sleep(0.3) # Telegram API flood-limitga tushmasligi uchun kichik pauza
        except Exception as e:
            print(f"--> [{i}/10] Bot reaksiyasida xatolik: {e}")

if __name__ == "__main__":
    while True:
        try:
            # Faqat 1 ta bot Telegram bilan bog'lanadi va postlarni ushlaydi
            main_bot.polling(non_stop=True, interval=2, timeout=20)
        except Exception as e:
            print(f"Ulanishda uzilish: {e}")
            time.sleep(5)
