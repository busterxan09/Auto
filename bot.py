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

# Railway konteyneri to'xtab qolmasligi uchun HTTP Health Check server
async def handle_ping(request):
    return web.Response(text="Botlar faol va ishlamoqda!")

async def start_health_check_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)
    
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Railway Health Check Server {port}-portda ishga tushdi.")

async def set_reaction(session, token, chat_id, message_id, emoji):
    url = f"https://api.telegram.org/bot{token}/setMessageReaction"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": emoji}]
    }
    try:
        async with session.post(url, json=payload, timeout=10) as resp:
            data = await resp.json()
            if data.get("ok"):
                print(f"[{emoji}] Reaksiya bosildi! Bot: {token[:10]}...")
            else:
                print(f"Xatolik ({token[:10]}...): {data.get('description')}")
    except Exception as e:
        print(f"Ulanish xatosi ({token[:10]}...): {e}")

async def listen_bot(session, bot_info):
    token = bot_info["token"]
    emoji = bot_info["emoji"]
    offset = 0

    print(f"Bot ishga tushdi: {token[:10]}...")

    while True:
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        params = {
            "offset": offset,
            "timeout": 20,
            "allowed_updates": ["channel_post"]
        }
        try:
            async with session.get(url, params=params, timeout=30) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for update in data.get("result", []):
                        offset = update["update_id"] + 1
                        if "channel_post" in update:
                            post = update["channel_post"]
                            chat_id = post["chat"]["id"]
                            message_id = post["message_id"]
                            await set_reaction(session, token, chat_id, message_id, emoji)
        except Exception:
            await asyncio.sleep(3)

        await asyncio.sleep(0.5)

async def main():
    # 1. Railway to'xtab qolmasligi uchun serverni yoqamiz
    await start_health_check_server()

    # 2. Botlarni ishga tushiramiz
    print("Barcha botlar Telegram bilan bog'lanmoqda...")
    timeout = aiohttp.ClientTimeout(total=35)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [listen_bot(session, bot) for bot in BOT_REACTIONS]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass



