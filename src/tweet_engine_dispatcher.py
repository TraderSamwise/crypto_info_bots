from constants import ELON_TWITTER_ACCOUNT_ID, DELTAONE_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID, \
    WHALEALERT_TWITTER_ACCOUNT_ID, LIVESQUAWK_TWITTER_ACCOUNT_ID, DB_TWITTER_ACCOUNT_ID, \
    COINBASE_PRO_TWITTER_ACCOUNT_ID, COINBASE_TWITTER_ACCOUNT_ID, CZ_TWITTER_ACCOUNT_ID
from tweet_engine_coinbase import tweet_engine_coinbase
# from tweet_engine_elon import tweet_engine_elon
from tweet_engine_news import tweet_engine_news
from tweet_engine_whalealert import tweet_engine_whalealert


def tweet_engine_dispatcher(status):
    if status.user.id_str in [CZ_TWITTER_ACCOUNT_ID, DELTAONE_TWITTER_ACCOUNT_ID, FIRSTSQUAWK_TWITTER_ACCOUNT_ID, LIVESQUAWK_TWITTER_ACCOUNT_ID, DB_TWITTER_ACCOUNT_ID]:
        tweet_engine_news(status)
    elif status.user.id_str == WHALEALERT_TWITTER_ACCOUNT_ID:
        tweet_engine_whalealert(status)
    elif status.user.id_str in [COINBASE_TWITTER_ACCOUNT_ID, COINBASE_PRO_TWITTER_ACCOUNT_ID]:
        tweet_engine_coinbase(status)