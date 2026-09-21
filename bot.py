import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import ReactionTypeEmoji

BOT_TOKEN = "8827183894:AAGzagONk1HfYdqyEmVISm_cggLr4mGjipE"
DEFAULT_REACTIONS = ["🔥"]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    me = await bot.get_me()
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="➕ Add My Channel",
                    url=f"https://t.me/{me.username}?startchannel=true",
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="📋 My Channels", callback_data="my_channels"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="❓ How It Works", callback_data="how_it_works"
                )
            ],
        ]
    )

    text = (
        "✅ **You're in! Welcome to Auto Reactions Bot** 🤖\n\n"
        "━━━━━━━\n"
        "🚀 **How to get reactions on your posts:**\n\n"
        "1️⃣ Tap **Add My Channel** below\n"
        "2️⃣ Make this bot an **Admin** in your channel\n"
        "3️⃣ Post anything — reactions appear automatically ❤️🔥😍👍\n"
        "━━━━━━━\n"
        "👇 **Get started:**"
    )

    await message.answer(text, parse_mode="Markdown", reply_markup=kb)


@dp.channel_post()
async def auto_react_to_channel_post(message: types.Message):
    try:
        reactions_to_set = [
            ReactionTypeEmoji(emoji=emoji) for emoji in DEFAULT_REACTIONS
        ]

        await bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=reactions_to_set,
            is_big=False,
        )
        logging.info(
            f"Reaksiya muvaffaqiyatli qo'yildi: {message.chat.id} - {message.message_id}"
        )
    except Exception as e:
        logging.error(f"Reaksiya qo'yishda xatolik: {e}")


async def main():
    me = await bot.get_me()
    await bot.delete_webhook(drop_pending_updates=True)
    print(f"Bot ishga tushdi: @{me.username}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
