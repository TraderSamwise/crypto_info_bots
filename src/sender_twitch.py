import asyncio
import datetime
import os
from threading import Thread

import ccxt
from twitchio.ext import commands

from custom_twitchio_bot import CustomTwitchBot

bot_account_name = "BOT_ACCOUNT_NAME"
token = os.getenv("TWITCH_OAUTH_TOKEN")
client_id = os.getenv("TWITCH_CLIENT_ID")

exchange_bybit = ccxt.bybit({
    'apiKey': os.environ.get('BYBIT_KEY'),
    'secret': os.environ.get('BYBIT_SECRET'),
    'enableRateLimit': True
})
exchange_bybit.load_markets()

exchange_ftx = ccxt.ftx({
    'apiKey': os.environ.get('FTX_KEY'),
    'secret': os.environ.get('FTX_SECRET'),
    'enableRateLimit': True
})
exchange_ftx.load_markets()

def format_usd(v):
    return "{:,}".format(round(float(v), 2))

def format_btc(v):
    return round(float(v), 4)

def format_side(v):
    v = v.lower()
    if (v == "sell"):
        return "Short"
    else:
        return "Long"

def format_bybit_positions(positions):
    msgs = []
    for pos in positions:
        msgs.append(f'[symbol: {pos["symbol"]}, side: {format_side(pos["side"])}, size: {format_usd(pos["size"])} USD, entry: {format_usd(pos["entry_price"])}, UnrlPNL: {format_btc(pos["unrealised_pnl"])}, RealPNL: {format_btc(pos["realised_pnl"])}]')
    return msgs

def format_ftx_size(v):
    return format_usd(str(abs(float(v))))

def format_ftx_positions(positions):
    msgs = []
    for pos in positions:
        msgs.append(f'[symbol: {pos["future"]}, side: {format_side(pos["side"])}, size: {format_ftx_size(pos["cost"])} USD, entry: {format_usd(pos["recentAverageOpenPrice"])}, B/E: {format_usd(pos["recentBreakEvenPrice"])}, PNL: {format_usd(pos["recentPnl"])} USD]')
    return msgs

class Bot(CustomTwitchBot):

    def __init__(self):
        super().__init__(irc_token=token, client_id=client_id, nick='botbotsamwise', prefix='!',
                         initial_channels=['tradersamwise'])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')
        self.chan = bot.get_channel("tradersamwise")
        print(self.chan)


    async def positions_helper(self, ctx):
        if not hasattr(self, "_notified_timeout"):
            self._notified_timeout = False
        if not hasattr(self, "_last_fetch_positions"):
            self._last_fetch_positions = datetime.datetime(2009, 1, 6, 15, 8, 24, 78915)
        now = datetime.datetime.now()
        if (now - self._last_fetch_positions).seconds < 60:
            if not self._notified_timeout:
                self._notified_timeout = True
                await ctx.send("Command is timed out...")
            return
        self._notified_timeout = False
        self._last_fetch_positions = now
        bybit_positions = exchange_bybit.v2_private_get_position_list()
        bybit_open_positions = [position['data'] for position in bybit_positions['result'] if position['data']['size'] != '0']
        # https://github.com/ccxt/ccxt/issues/9213
        ftx_positions = exchange_ftx.private_get_positions({'showAvgPrice': False})
        ftx_open_positions = [position for position in ftx_positions['result'] if position['size'] != '0.0']
        bybit_msgs = format_bybit_positions(bybit_open_positions)
        for msg in bybit_msgs:
            await ctx.send("ByBit: " + msg)
        ftx_msgs = format_ftx_positions(ftx_open_positions)
        for msg in ftx_msgs:
            await ctx.send("FTX: " + msg)
        if len(bybit_msgs) == 0 and len (ftx_msgs) == 0:
            await ctx.send("No open positions.")

    # Commands use a different decorator
    @commands.command(name='positions')
    async def positions(self, ctx):
        await self.positions_helper(ctx)

    # Commands use a different decorator
    @commands.command(name='position')
    async def position(self, ctx):
        await self.positions_helper(ctx)

        # Commands use a different decorator
    @commands.command(name='pos')
    async def pos(self, ctx):
        await self.positions_helper(ctx)


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





