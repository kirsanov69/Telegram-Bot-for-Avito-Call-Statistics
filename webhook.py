from fastapi import FastAPI
from pydantic import BaseModel
from handlers import *
import requests
from config import load_config
import logging
from tg_message_data import Update

app = FastAPI()

class TelegramWebhook(BaseModel):
    message: dict = {}
    callback_query: dict = {}
    message: dict = {}
    pre_checkout_query: dict = {}
    success_payment: dict = {}


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("webhook.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@app.post("/webhook")
async def webhook_handler(update: Update):
    logger.info(f'Received data: {update}')
    print('update:', update)

    try:
        if update.message:
            if update.message.text:
                text = update.message.text
                if text == "/start ":
                    await handle_send_token(update.message)

        if update.callback_query:
            callback_query = update.callback_query
            callback_data = callback_query.data
            if callback_data.startswith("stat"):
                await handle_show_stats(callback_query)

        logger.info('Status: ok')
        return {"status": "ok"}

    except Exception as e:
        logger.exception(f"Error in webhook handler: {e}")
        return {"status": "error", "message": str(e)}

#  обработчик для корневого URL
@app.get("/")
async def read_root():
    logger.info('Root endpoint reached')
    return {"message": "Welcome to the Telegram Webhook Server"}

#  обработчик для favicon.ico
@app.get("/favicon.ico")
async def favicon():
    return {"status": "ok"}


if __name__ == '__main__':
    config = load_config('config')
    TOKEN = config.tg_bot.token
    WEBHOOK_URL = config.webhook_url.url


    # Настройка вебхука
    url = f'https://api.telegram.org/bot{TOKEN}/setWebhook'
    payload = {
        'url': WEBHOOK_URL,
        'allowed_updates': ["message", "callback_query", "pre_checkout_query", "successful_payment"]
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("Webhook set successfully")
    else:
        print(f"Failed to set webhook: {response.text}")

    # Запуск сервера FastAPI на порту 5000
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
