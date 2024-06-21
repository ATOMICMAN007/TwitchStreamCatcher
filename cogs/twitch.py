import asyncio
import logging

import discord
from discord.ext.commands import Cog, Context, command

from TwitchStreamCatcher import TwitchStreamCatcher

# from discord.ext import tasks


logger = logging.getLogger(__name__)


class Twitch(Cog):
    def __init__(self, bot: TwitchStreamCatcher):
        self.bot = bot

    # TODO: Make the game arg take mutiple games to fetch
    @command()
    async def live(self, ctx: Context, game: str):
        try:
            game = int(game)
            logger.info("Fetching game streams for: {game}")
            streams = await self.bot.twitch_api.fetch_streams(game_ids=[game])
            logger.info(streams)
            stream_ids = [stream.user.id for stream in streams]
            streamers = await self.bot.twitch_api.fetch_users(ids=stream_ids)

            streamer_ids = {streamer.id: streamer.name for streamer in streamers}

            stream_msgs = []
            streamer_names = []
            streamer_links = []
            for stream in streams:
                streamer_name = streamer_ids.get(stream.user.id, "none")
                # stream_msg = (
                #     f"{stream.user.name}(https://www.twitch.tv/{streamer_name})"
                # )

                # stream_msgs = stream_msgs + "\n" + stream_msg
                # stream_msgs.append(
                #     f"{stream.user.name}(https://www.twitch.tv/{streamer_name})"
                # )

                streamer_names.append(stream.user.name)
                streamer_links.append(f"https://www.twitch.tv/{streamer_name}")
            # Send in chunks using embeds
            embed_limit = 25  # Number of fields per embed
            chunks = [
                stream_msgs[i : i + embed_limit]
                for i in range(0, len(stream_msgs), embed_limit)
            ]

            for chunk in chunks:
                embed = discord.Embed(
                    title="Live Streamers",
                    description="Streamers currently playing the game",
                )
                for stream_msg in chunk:
                    embed.add_field(name="\u200b", value=stream_msg, inline=False)

                await ctx.send(embed=embed)
                await asyncio.sleep(
                    1
                )  # Adding a 1 second delay between messages to avoid rate limits

            logger.info("---")
            logger.info(streamers)
            logger.info(f"--- Length: {len(streamers)}")
            logger.info(stream_msgs)
            logger.info(f"--- Length: {len(stream_msgs)}")
            logger.info("---")
            logger.info("---")
            logger.info("---")

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            await ctx.send("An error occurred while fetching live streams.")
            # msg = ""
            # for stream in streams:
            #     msg = (
            #         msg
            #         + "\n"
            #         + f"{stream.user.name} (https://www.twitch.tv/{stream.user.id}) is live since {stream.started_at}"
            #     )
            # await ctx.send(stream_msgs)

        # except ValueError:
        #     await ctx.send("Enter a valid game id.", ephemeral=True)

    @command()
    async def ping(self, ctx: Context):
        await ctx.send("Pong")

    # @tasks.loop(seconds=5)
    # async def get_game_streams(self):
    #     await self.bot.twitch_api.fetch_streams()


async def setup(bot: TwitchStreamCatcher):
    await bot.add_cog(Twitch(bot))
