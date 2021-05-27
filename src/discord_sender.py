import os
import requests

def send_to_discord(msg, webhook_url):
    response = requests.post(webhook_url, json=msg)
    return response

def send_msg_to_discord(content, webhook):
    webhook_url = os.getenv(webhook)
    return send_to_discord({"content": content}, webhook_url)
    # pass
