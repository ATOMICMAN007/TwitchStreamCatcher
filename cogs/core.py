import logging

from discord.ext.commands import Cog, Context, ExtensionError, command

from TwitchStreamCatcher import TwitchStreamCatcher

# import os


logger = logging.getLogger(__name__)


class Core(Cog):
    def __init__(self, bot: TwitchStreamCatcher):
        self.bot = bot

    @command(aliases=["stop", "quit"])
    async def shutdown(self, ctx: Context):
        logger.info("Bot shutting down")
        await ctx.send("Bot shutting down", ephemeral=True)
        await self.bot.close()

    # @command(hidden=True)
    # async def load(self, ctx: Context, *, module: str):
    #     """Loads a module."""
    #     try:
    #         await self.bot.load_extension(module)
    #     except ExtensionError as e:
    #         await ctx.send(f"{e.__class__.__name__}: {e}")
    #     else:
    #         await ctx.send("\N{OK HAND SIGN}")
    #
    # @command(hidden=True)
    # async def unload(self, ctx: Context, *, module: str):
    #     """Unloads a module."""
    #     try:
    #         await self.bot.unload_extension(module)
    #     except ExtensionError as e:
    #         await ctx.send(f"{e.__class__.__name__}: {e}")
    #     else:
    #         await ctx.send("\N{OK HAND SIGN}")
    #
    # @command(name="reload", hidden=True, invoke_without_command=True)
    # async def _reload(self, ctx: Context, *, module: str):
    #     """Reloads a module."""
    #     try:
    #         await self.bot.reload_extension(module)
    #     except ExtensionError as e:
    #         await ctx.send(f"{e.__class__.__name__}: {e}")
    #     else:
    #         await ctx.send("\N{OK HAND SIGN}")

    @command(aliases=["load_extension", "load_cog"])
    async def load(self, ctx: Context, cog: str = None):
        try:
            logger.info(type(cog))
            await self.bot.load_extension(f"cogs.{cog}")
            logger.info(f"Loading Cog: {cog}")
            await ctx.message.add_reaction("\N{OK HAND SIGN}")
        except ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")

    @command(aliases=["unload_extension", "unload_cog"])
    async def unload(self, ctx: Context, cog: str = None):
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            logger.info(f"Unloading Cog: {cog}")
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        except ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")

    @command(aliases=["reload_extension", "reload_cog"])
    async def reload(self, ctx: Context, cog: str = None):
        try:
            logger.info(cog)
            await self.bot.reload_extension(f"cogs.{cog}")
            logger.info(f"Reloading Cog: {cog}")
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        except ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")


async def setup(bot: TwitchStreamCatcher):
    await bot.add_cog(Core(bot))
