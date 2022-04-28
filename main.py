import asyncio
from asyncio import AbstractEventLoop
from typing import Any

from discord import Permissions
from discord.ext.commands import Bot
import discord
import platform

from config import Config


class DiscordBot(Bot):
    def __init__(self, command_prefix, *, config: Config, **options: Any):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix, intents=intents, **options)

        self.config = config

    @property
    def invite_url(self) -> str:
        return discord.utils.oauth_url(
                self.user.id,
                permissions=Permissions(
                        add_reactions=True,
                        read_messages=True
                ),
                scopes=('bot', 'applications.commands')
        )

    async def on_ready(self):
        print('Logged on as', self.user)
        print('Registering commands...')

        for guild in self.guilds:
            # Remove commands from guild
            self.tree.clear_commands(guild=guild)
            await self.tree.sync(guild=guild)

            # Sync guild only commands
            await self.tree.sync(guild=guild)

        # Sync global commands
        await self.tree.sync()

        print('Startup finished!')
        print(f"Invite: {self.invite_url}")


async def startup(loop: AbstractEventLoop):
    config = Config()

    async with DiscordBot(command_prefix="!", config=config, loop=loop) as bot:
        await bot.load_extension("clip_mirror_cog")

        await bot.start(config.get("DISCORD_TOKEN"))


if __name__ == '__main__':
    loop = None

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

    try:
        asyncio.run(startup(loop=loop))
    except KeyboardInterrupt:
        pass
