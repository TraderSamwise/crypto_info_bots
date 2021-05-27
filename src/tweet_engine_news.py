import os
from imageai.Detection.Custom import CustomObjectDetection
import urllib
import time

from constants import ELON_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID, DELTAONE_TWITTER_ACCOUNT_ID
from discord_sender import send_msg_to_discord


# Return path to a given file based on current directory
from telegram_sender import send_to_telegram

# Keywords to detect
keywords = ["coin", "doge", "crypto", "bitcoin", "coinbase", "bitmex", "gemini", "kraken", "binance", "token",
            "cryptocurrency", "altcoin", "altcoins", "eth", "ethereum", "coins"]


def tweet_engine_news(status):
    if status.user.id_str in [DELTAONE_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID] and any(tweet in status.text.lower() for tweet in keywords):
        if (status.user.id_str == DELTAONE_TWITTER_ACCOUNT_ID):
            auth = "Bloomberg (DeltaOne)"
        elif (status.user.id_str == FIRSTSQUAWK_TWITTER_ACCOUNT_ID):
            auth = "FirstSquawk"
        msg = f"{auth} tweeted: \"{status.text}\" - on {time.ctime()}. Tweet: https://twitter.com/twitter/statuses/{status.id}"
        print(msg)
        send_to_telegram("@SamwiseNewsBot", msg)
        send_msg_to_discord(msg)
