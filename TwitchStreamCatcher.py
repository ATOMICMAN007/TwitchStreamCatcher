import logging
import os

from aiohttp import ClientSession
from discord.ext.commands import (Bot, BotMissingPermissions, CommandError,
                                  CommandNotFound, Context,
                                  MissingRequiredArgument, NoPrivateMessage)
from twitchio import Client

logger = logging.getLogger(__name__)


class TwitchClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def event_ready(self):
        logger.info('Connected to Twitch')

    async def event_reconnect(self):
        logger.info('Reconnection to Twitch')

    async def close(self):
        logger.info('Closing Twitch client connection')
        await super().close()


class TwitchStreamCatcher(Bot):
    def __init__(self, web_session: ClientSession, twitch_client_id: str, twitch_client_secret: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.web_client = web_session
        self._twitch_client_id = twitch_client_id
        self._twitch_client_secret = twitch_client_secret

    async def on_ready(self):
        logger.info(f'{self.user.name} is online')

    async def setup_hook(self):
        try:
            cogs = next(os.walk('cogs'))[2]
            cogs = [c.split('.')[0] for c in cogs]

        except FileNotFoundError:
            logger.info('Cogs could not be loaded, continuing without them.')

        for cog in cogs:
            # TODO: Find out the different errors `load_extension` can throw and continue loading other cogs if one fails
            await self.load_extension(f"cogs.{cog}")

        self.twitch_api = TwitchClient.from_client_credentials(self._twitch_client_id, self._twitch_client_secret)

    async def on_command(self, ctx: Context):
        if ctx.command:
            logger.info(f'{ctx.author.global_name} ran a command: {ctx.command.name}')

    async def on_command_error(self, ctx: Context, err: CommandError):
        # Ignore if local handler present
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog and cog._get_overridden_method(cog.cog_command_error):
            return

        match err:
            case CommandNotFound():
                await ctx.send("Command does not exist.", ephemeral=True)

            case BotMissingPermissions():
                perm = err.missing_permissions
                await ctx.send('Insufficient permissions. Missing permission', perm)
                logger.error(f'Insufficient permission to run {ctx.command.name}. Missing permission {perm}')
                logger.error(f'Command used in {ctx.guild.name} ID: {ctx.guild.id}')

            case NoPrivateMessage():
                await ctx.send("This command cannot be used in DMs", ephemeral=True)

            case MissingRequiredArgument():
                await ctx.send("Missing required argument(s)", ephemeral=True)

            case _:
                await ctx.send("Something went wrong.")

                if ctx.prefix and ctx.invoked_with:
                    content = ctx.message.content.removeprefix(ctx.prefix + ctx.invoked_with).strip()
                else:
                    content = ctx.message.content

                logger.error(f'Something went wrong with {ctx.command.name}. Error: {err}')
                logger.error(f'Message: {content}. User: {ctx.author.global_name}')

    async def close(self):
        # await self.twitch_api.close()
        await self.web_client.close()
        await super().close()

