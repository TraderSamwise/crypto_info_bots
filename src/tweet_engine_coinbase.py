import time

from constants import COINBASE_TWITTER_ACCOUNT_ID, COINBASE_PRO_TWITTER_ACCOUNT_ID
from sender_discord import send_msg_to_discord
# Return path to a given file based on current directory
from sender_telegram import send_to_telegram
# Keywords to detect
from sender_twitch import send_to_twitch

keywords = ["starting today"]


def tweet_engine_coinbase(status):
    if any(tweet in status.text.lower() for tweet in keywords):
        if (status.user.id_str == COINBASE_TWITTER_ACCOUNT_ID):
            auth = "Coinbase"
        elif (status.user.id_str == COINBASE_PRO_TWITTER_ACCOUNT_ID):
            auth = "Coinbase Pro"
        msg = f"{auth} tweeted: \"{status.text}\" - on {time.ctime()}. Tweet: https://twitter.com/twitter/statuses/{status.id}"
        print(msg)
        send_to_telegram("@SamwiseNewsBot", msg)
        send_to_twitch(msg)
        send_msg_to_discord(msg, "PRIMARY_DISCORD_WEBHOOK_URL")
