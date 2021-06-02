import os
from imageai.Detection.Custom import CustomObjectDetection
import urllib
import time

from apiconfig import get_tweepy_api
from constants import ELON_TWITTER_ACCOUNT_ID
from sender_discord import send_msg_to_discord


# Return path to a given file based on current directory
from sender_telegram import send_to_telegram
from sender_twitch import send_to_twitch


def get_current_path(filename: str):
    if "src" in os.getcwd():
        return os.path.join(os.path.dirname(os.getcwd()), filename)
    else:
        return os.path.join(os.getcwd(), filename)


# ImageAi
detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(get_current_path("doge-ai.h5"))
detector.setJsonPath(get_current_path("detection_config.json"))
detector.loadModel()

# Keywords to detect
keywords = ["stock", "share", "$", "doge", "crypto", "bitcoin", "ethereum", " eth ", "energy", "moon"]
ai_result = None

def get_thread(status):
    twitter_thread = []
    tweep_api = get_tweepy_api()
    curr_status = status
    while True:
        if not  curr_status['in_reply_to_status_id']:
            break
        curr_status = tweep_api.get_status(curr_status['in_reply_to_status_id'])
        twitter_thread.append(curr_status)
    return twitter_thread

def check_tweet_for_keyword(status):
    return any(tweet in status['text'].lower() for tweet in keywords)

def check_tweet_for_image(status):
    if "extended_entities" in status:
        # Loop through each image
        for media in status['extended_entities']['media']:
            """
            Download and write the tweet image.
            This will overwrite each new tested image to
            reduce the number of files stored.
            """
            urllib.request.urlretrieve(
                media["media_url_https"], "image-to-test.jpg"
            )
            # Run the image through ImageAI to detect objects in it
            detections = detector.detectObjectsFromImage(
                input_image=os.path.join(os.getcwd(), "image-to-test.jpg"),
                output_image_path=os.path.join(os.getcwd(), "image-tested.jpg"),
            )
            # If detection data matches any of the keywords send e-mail
            for detection in detections:
                if any(name in detection["name"] for name in keywords):
                    return True
    return False

def tweet_engine_elon(status):
    # convert to dict bc rest api to fetch thread uses dict
    status = status.__dict__

    # check if elon tweet itself matches criteria
    if check_tweet_for_keyword(status):
        msg = f"Elon tweeted: \"{status['text']}\" - on {time.ctime()}. Tweet: https://twitter.com/twitter/statuses/{status['id']}"
        print(msg)
        send_to_telegram("@SamwiseElonBot", msg)
        send_to_twitch(msg)
        send_msg_to_discord(msg, "PRIMARY_DISCORD_WEBHOOK_URL")
    elif check_tweet_for_image(status):
        msg = f'Elon tweeted image  - on {time.ctime()}. Tweet: {status["text"]}'
        print(msg)
        send_to_telegram("@SamwiseElonBot", msg)
        send_to_twitch(msg)
        send_msg_to_discord(msg, "PRIMARY_DISCORD_WEBHOOK_URL")
    # check if thread itself matches criteria
    else:
        twitter_thread = get_thread(status)
        for thread_status in twitter_thread:
            if check_tweet_for_keyword(thread_status) or check_tweet_for_image(thread_status) or any(tweet in thread_status['user']['name'] for tweet in keywords):
                msg = f"Elon responded to a crypto tweet: \"{status['text']}\" - on {time.ctime()}. Tweet: https://twitter.com/twitter/statuses/{status['id']}"
                print(msg)
                send_to_telegram("@SamwiseElonBot", msg)
                send_to_twitch(msg)
                send_msg_to_discord(msg, "PRIMARY_DISCORD_WEBHOOK_URL")
                return
