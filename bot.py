import asyncio

import discord
from aiohttp import ClientSession
from dotenv import dotenv_values

from TwitchStreamCatcher import TwitchStreamCatcher

# from twitchio import Client as TwitchClient


async def main():
    config = dotenv_values(".env")
    intents = discord.Intents.default()
    intents.message_content = True
    discord.utils.setup_logging()

    async with ClientSession() as session:
        # twitch_api = TwitchClient.from_client_credentials(client_id=config['twitch_clientid'], client_secret=config['twitch_authid'])
        async with TwitchStreamCatcher(
            web_session=session,
            twitch_client_id=config["twitch_clientid"],
            twitch_client_secret=config["twitch_clientsecret"],
            command_prefix=".",
            intents=intents,
        ) as bot:
            await bot.start(config["discord_token"])


if __name__ == "__main__":
    asyncio.run(main())
