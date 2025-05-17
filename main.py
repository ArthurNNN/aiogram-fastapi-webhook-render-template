from fastapi import FastAPI
import time
import logging
import os

from aiogram import Bot, Dispatcher, types

# ENV
TOKEN = os.getenv('TOKEN')
RENDER_WEB_SERVICE_NAME = os.getenv('YOUR_RENDER_WEB_SERVICE_NAME')
WEBHOOK_URL = f"https://{RENDER_WEB_SERVICE_NAME}.onrender.com/webhook"

# Setup
logging.basicConfig(filemode='a', level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
app = FastAPI()

# Webhook startup
@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

# Telegram handlers
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply(f"Hello, {message.from_user.full_name}!")

@dp.message_handler()
async def main_handler(message: types.Message):
    try:
        await message.reply("Hello world!")
    except Exception as e:
        logging.exception("Error in main_handler")
        await message.reply("Something went wrong...")

# Telegram webhook route
@app.post("/webhook")
async def webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)
    return {"status": "ok"}

# Health check
@app.get("/")
def main_web_handler():
    return "Everything ok!"

# Shutdown
@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
