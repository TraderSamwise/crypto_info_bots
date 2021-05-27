import os

from telegram import Bot
from telegram.utils.request import Request


request = Request(connect_timeout=120, read_timeout=120)
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=telegram_token, request=request)

def send_to_telegram(*args):
    return bot.send_message(*args)