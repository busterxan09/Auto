import asyncio
import os
import aiohttp
from aiohttp import web

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

async def send_single_reaction(session, token, chat_id, message_id, emoji):
    url = f"https://api.telegram.org/bot{token}/setMessageReaction"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": emoji}]
    }
    try:
        async with session.post(url, json=payload, timeout=5) as resp:
            res = await resp.json()
            if res.get("ok"):
                print(f"[{emoji}] Reaksiya qo'yildi! Bot: {token[:10]}...")
            else:
                print(f"Xato ({token[:10]}...): {res.get('description')}")
    except Exception as e:
        print(f"Ulanish xatosi ({token[:10]}...): {e}")

async def start_polling():
    master_token = BOT_REACTIONS[0]["token"]
    
    async with aiohttp.ClientSession() as session:
        # Eski webhookni tozalash
        await session.post(f"https://api.telegram.org/bot{master_token}/deleteWebhook")
        
        offset = 0
        print("Polling ishga tushdi! Yangi postlar kutilmoqda...")
        
        while True:
            try:
                url = f"https://api.telegram.org/bot{master_token}/getUpdates?offset={offset}&timeout=10"
                async with session.get(url, timeout=15) as resp:
                    data = await resp.json()
                    
                    if data.get("ok"):
                        for update in data.get("result", []):
                            offset = update["update_id"] + 1
                            post = update.get("channel_post") or update.get("edited_channel_post")
                            
                            if post:
                                chat_id = post["chat"]["id"]
                                message_id = post["message_id"]
                                print(f"Yangi post topildi! ID: {message_id}")
                                
                                tasks = [
                                    send_single_reaction(session, bot["token"], chat_id, message_id, bot["emoji"])
                                    for bot in BOT_REACTIONS
                                ]
                                await asyncio.gather(*tasks)
            except Exception as e:
                print(f"Polling xatosi: {e}")
            await asyncio.sleep(1)

async def handle_health(request):
    return web.Response(text="OK", status=200)

async def main():
    app = web.Application()
    app.router.add_get("/", handle_health)
    
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Server {port}-portda ishlamoqda...")

    # Pollingni alohida fonda yurgizish
    asyncio.create_task(start_polling())
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
