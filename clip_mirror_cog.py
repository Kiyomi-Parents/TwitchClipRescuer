import ftplib
import re
from pathlib import Path

from discord import Message, PartialEmoji
from discord.ext import commands
from discord.ext.commands import Cog

import downloader

from main import DiscordBot


async def setup(bot: DiscordBot):
    await bot.add_cog(ClipMirrorCog(bot))


class ClipMirrorCog(Cog):
    def __init__(self, bot: DiscordBot):
        self.bot = bot
        self.ftp_server = ftplib.FTP()

    _PATTERNS = (
        r".*((https://)?(clips.twitch.tv)/[\w-]+)",
        r".*((https://)?(www.twitch.tv)/(\w+)/clip/[\w-]+)"
    )

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.channel.id not in self.bot.config.get("CLIPS_CHANNEL_IDS"):
            return

        if message.author == self.bot.user:
            return

        target_directory = Path(f"{self.bot.config.get('FTP_DIRECTORY')}/{message.channel.name}")

        for pattern in self._PATTERNS:
            m = re.match(pattern, message.content)
            if m:
                self.ftp_server.connect(
                    self.bot.config.get("FTP_HOST"),
                    self.bot.config.get("FTP_PORT")
                )
                self.ftp_server.login(
                    self.bot.config.get("FTP_USERNAME"),
                    self.bot.config.get("FTP_PASSWORD")
                )
                downloader.download_clip(m.group(0), target_directory, self.ftp_server)
                self.ftp_server.quit()
                await message.add_reaction(PartialEmoji(name="✅"))
                break
