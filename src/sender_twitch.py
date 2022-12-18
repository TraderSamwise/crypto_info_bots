import asyncio
import os
from threading import Thread

from custom_twitchio_bot import CustomTwitchBot

bot_account_name = "BOT_ACCOUNT_NAME"
token = os.getenv("TWITCH_OAUTH_TOKEN")
client_id = os.getenv("TWITCH_CLIENT_ID")

class Bot(CustomTwitchBot):

    def __init__(self):
        super().__init__(irc_token=token, client_id=client_id, nick='botbotsamwise', prefix='!',
                         initial_channels=['tradersamwise', 'botbotsamwise'])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')
        self.chan = bot.get_channel("tradersamwise")
        print(self.chan)


    def send_message_direct(self, message):
        chan = self.chan
        print(chan)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(chan.send(message))


bot = Bot()
t = Thread(target=bot.run)
t.start()

def send_to_twitch(msg):
    return bot.send_message_direct(msg)
    # pass





