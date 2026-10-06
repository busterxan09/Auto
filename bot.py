import asyncio
import os
import aiohttp
from aiohttp import web

# Railway domeningiz
DOMAIN = "worker-production-a852.up.railway.app"

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

# Reaksiya bosish funksiyasi
async def send_single_reaction(session, token, chat_id, message_id, emoji):
    url = f"https://api.telegram.org/bot{token}/setMessageReaction"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": emoji}]
    }
    try:
        async with session.post(url, json=payload, timeout=10) as resp:
            res = await resp.json()
            if res.get("ok"):
                print(f"[{emoji}] Reaksiya muvaffaqiyatli qo'yildi! Bot: {token[:10]}...")
            else:
                print(f"Reaksiya xatosi ({token[:10]}...): {res.get('description')}")
    except Exception as e:
        print(f"Ulanishda xatolik ({token[:10]}...): {e}")

# Webhook orqali yangi postlarni qabul qilish
async def handle_webhook(request):
    try:
        data = await request.json()
        if "channel_post" in data:
            post = data["channel_post"]
            chat_id = post["chat"]["id"]
            message_id = post["message_id"]
            
            print(f"Yangi post qabul qilindi! Post ID: {message_id}, Chat ID: {chat_id}")
            
            async with aiohttp.ClientSession() as session:
                tasks = [
                    send_single_reaction(session, bot["token"], chat_id, message_id, bot["emoji"])
                    for bot in BOT_REACTIONS
                ]
                await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Webhook ishlov berishda xato: {e}")
        
    return web.Response(text="OK", status=200)

async def handle_health(request):
    return web.Response(text="Botlar faol rejimda!", status=200)

# Telegram Webhook o'rnatish
async def setup_webhook(app):
    master_token = BOT_REACTIONS[0]["token"]
    webhook_url = f"https://{DOMAIN}/webhook"
    
    url = f"







