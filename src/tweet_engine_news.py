import time

from constants import FIRSTSQUAWK_TWITTER_ACCOUNT_ID, DELTAONE_TWITTER_ACCOUNT_ID, \
    LIVESQUAWK_TWITTER_ACCOUNT_ID, DB_TWITTER_ACCOUNT_ID, CZ_TWITTER_ACCOUNT_ID
from sender_discord import send_msg_to_discord
# Return path to a given file based on current directory
from sender_telegram import send_to_telegram
# Keywords to detect
from sender_twitch import send_to_twitch

keywords = ["coin", "doge", "crypto", "bitcoin", "coinbase", "bitmex", "gemini", "kraken", "binance", "digital token", "blockchain",
            "cryptocurrency", "altcoin", "altcoins", " eth ", "ethereum", "coins", "bitconnect"]


def tweet_engine_news(status):
    if any(tweet in status.text.lower() for tweet in keywords):
        if (status.user.id_str == CZ_TWITTER_ACCOUNT_ID):
            auth = "CZ"
        elif (status.user.id_str == DELTAONE_TWITTER_ACCOUNT_ID):
            auth = "Bloomberg (DeltaOne)"
        elif (status.user.id_str == FIRSTSQUAWK_TWITTER_ACCOUNT_ID):
            auth = "FirstSquawk"
        elif (status.user.id_str == LIVESQUAWK_TWITTER_ACCOUNT_ID):
            auth = "LiveSquawk"
        elif (status.user.id_str == DB_TWITTER_ACCOUNT_ID):
            auth = "db (tier10k)"
        msg = f"{auth} tweeted: \"{status.text}\" - on {time.ctime()}. Tweet: https://twitter.com/twitter/statuses/{status.id}"
        print(msg)
        send_to_telegram("@SamwiseNewsBot", msg)
        send_to_twitch(msg)
        send_msg_to_discord(msg, "SAMWISE_NEWS_DISCORD_WEBHOOK_URL")
        send_msg_to_discord(msg, "SECRET_NEWS_DISCORD_WEBHOOK_URL")
        send_msg_to_discord(msg, "NINJASCALP_NEWS_DISCORD_WEBHOOK_URL")
