import asyncio
import datetime
import os
from threading import Thread

import ccxt
from twitchio.ext import commands
from twitchio.ext.commands import CheckFailure
from twitchio.ext.commands.stringparser import StringParser

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
    return round(float(v), 2)

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
        msgs.append(f'[symbol: {pos["symbol"]}, side: {format_side(pos["side"])}, size: {format_usd(pos["size"])} USD, entry: {format_usd(pos["entry_price"])}, UnrlPNL: {format_btc(pos["unrealised_pnl"])}]')
    return msgs


def format_ftx_positions(positions):
    msgs = []
    for pos in positions:
        msgs.append(f'[symbol: {pos["future"]}, side: {format_side(pos["side"])}, size: {pos["size"]}, entry: {pos["entryPrice"]}]')
    return msgs

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=token, client_id=client_id, nick='botbotsamwise', prefix='!',
                         initial_channels=['tradersamwise'])


    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')
        self.chan = bot.get_channel("tradersamwise")
        print(self.chan)

    async def event_message(self, message):
        # print(message.content)
        # await self.send_message_direct("dude")
        # print(message)
        try:
            await self.handle_commands(message)
        except Exception as e:
            print(e)

    async def handle_commands(self, message, ctx=None):
        if ctx is None:
            try:
                ctx = await self.get_context(message)
            except Exception as e:
                return await self.event_error(e, message.raw_data)

        if not ctx.prefix:
            return

        content = message.content
        content = content[len(ctx.prefix)::].lstrip(' ')
        parsed = StringParser().process_string(content)

        message.clean_content = ' '.join(parsed.values())

        try:
            command = parsed.pop(0)
        except KeyError:
            return

        try:
            command = self._aliases[command]
        except KeyError:
            pass

        try:
            if command in self.commands:
                command = self.commands[command]
            elif command:
                return
        except Exception as e:
            ctx.command = None
            return await self.event_command_error(ctx, e)

        ctx.command = command
        instance = ctx.command.instance

        try:
            result = await self._handle_checks(ctx, command.no_global_checks)
        except Exception as e:
            return await self.event_command_error(ctx, e)
        else:
            if callable(result):
                return await self.event_command_error(ctx, CheckFailure(f'The command <{command.name}> failed to invoke'
                                                                        f' due to checks:: {result.__name__}'))
            elif not result:
                raise CheckFailure(f'The command <{command.name}> failed to invoke due to checks.')

        try:
            ctx.args, ctx.kwargs = await command.parse_args(instance, parsed)

            await self.global_before_hook(ctx)

            if ctx.command._before_invoke:
                await ctx.command._before_invoke(instance, ctx)

            if instance:
                await ctx.command._callback(instance, ctx, *ctx.args, **ctx.kwargs)
            else:
                await ctx.command._callback(ctx, *ctx.args, **ctx.kwargs)
        except Exception as e:
            if ctx.command.on_error:
                await ctx.command.on_error(instance, ctx, e)

            await self.event_command_error(ctx, e)

        try:
            # Invoke our after command hooks...
            if command._after_invoke:
                await ctx.command._after_invoke(ctx)
            await self.global_after_hook(ctx)
        except Exception as e:
            await self.event_command_error(ctx, e)


    async def positions_helper(self, ctx):
        if not hasattr(self, "_last_fetch_positions"):
            self._last_fetch_positions = datetime.datetime(2009, 1, 6, 15, 8, 24, 78915)
        now = datetime.datetime.now()
        if (now - self._last_fetch_positions).seconds < 15:
            return
        self._last_fetch_positions = now
        bybit_positions = exchange_bybit.v2_private_get_position_list()
        bybit_open_positions = [position['data'] for position in bybit_positions['result'] if position['data']['size'] != '0']
        ftx_positions = exchange_ftx.fetch_positions()
        ftx_open_positions = [position for position in ftx_positions if position['size'] != '0.0']
        # msg = f'Bybit: {ctx.author.name}!'
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





