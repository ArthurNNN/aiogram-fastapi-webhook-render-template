from fastapi import FastAPI, Request
import time
import logging
import os

from aiogram import Bot, Dispatcher, types

# ENV
TOKEN = os.getenv('TOKEN')
RENDER_WEB_SERVICE_NAME = os.getenv('YOUR_RENDER_WEB_SERVICE_NAME')
WEBHOOK_URL = f"https://{RENDER_WEB_SERVICE_NAME}.onrender.com/webhook"

# Logging config
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
app = FastAPI()


@app.on_event("startup")
async def on_startup():
    logging.info("Bot startup initiated.")
    try:
        webhook_info = await bot.get_webhook_info()
        logging.info(f"Current webhook: {webhook_info.url}")
        if webhook_info.url != WEBHOOK_URL:
            await bot.set_webhook(url=WEBHOOK_URL)
            logging.info(f"Webhook set to: {WEBHOOK_URL}")
        else:
            logging.info("Webhook already correctly set.")
    except Exception as e:
        logging.error(f"Error during webhook setup: {e}")


@app.on_event("shutdown")
async def on_shutdown():
    logging.info("Shutting down bot session.")
    await bot.session.close()
    logging.info("Bot session closed.")


@app.get("/")
def main_web_handler():
    logging.info("Health check called: '/' route hit.")
    return "Everything ok!"


@app.post("/webhook")
async def webhook(request: Request):
