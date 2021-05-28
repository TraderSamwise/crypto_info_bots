import asyncio
import os
from threading import Thread

from twitchio.ext import commands

bot_account_name = "BOT_ACCOUNT_NAME"
token = os.getenv("TWITCH_OAUTH_TOKEN")
client_id = os.getenv("TWITCH_CLIENT_ID")

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=token, client_id=client_id, nick='botbotsamwise', prefix='&',
                         initial_channels=['tradersamwise'])


    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')
        self.chan = bot.get_channel("tradersamwise")
        print(self.chan)

    async def event_message(self, message):
        # print(message.content)
        # await self.send_message_direct("dude")
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

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





