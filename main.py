import asyncio
from typing import Any

from discord.ext.commands import Bot
import discord

from config import Config


class DiscordBot(Bot):
    def __init__(self, command_prefix, *, config: Config, **options: Any):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix, intents=intents, **options)

        self.config = config

    async def on_ready(self):
        print('Logged on as', self.user)

        for guild in self.guilds:
            self.tree.clear_commands(guild=guild)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)


async def startup():
    config = Config()

    async with DiscordBot(command_prefix="!", config=config) as bot:
        await bot.load_extension("clip_mirror_cog")

        await bot.start(config.get("DISCORD_TOKEN"))


if __name__ == '__main__':
    asyncio.run(startup())
