from twitchio.ext.commands import CheckFailure
from twitchio.ext.commands.stringparser import StringParser
from twitchio.ext import commands

class CustomTwitchBot(commands.Bot):

    async def event_message(self, message):
        # print(message.content)
        # await self.send_message_direct("dude")
        # print(message)
        try:
            if message.channel.name == 'botbotsamwise' and message.content == 'HeyGuys':
                try:
                    ctx = await self.get_context(message)
                    await self.positions_helper(ctx)
                except Exception as e:
                    return await self.event_error(e, message.raw_data)
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