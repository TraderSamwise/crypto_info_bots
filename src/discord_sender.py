import os
import requests

def send_to_discord(msg):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    response = requests.post(webhook_url, json=msg)
    return response

def send_msg_to_discord(content):
    return send_to_discord({"content": content})
    # pass
