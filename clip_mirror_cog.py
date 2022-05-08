import ftplib
import re
from pathlib import Path
from typing import List

import discord
from discord import Message, PartialEmoji, app_commands, TextChannel, Permissions
from discord.app_commands import MissingPermissions
from discord.ext import commands
from discord.ext.commands import Cog

import downloader
from main import DiscordBot


async def setup(bot: DiscordBot):
    await bot.add_cog(ClipMirrorCog(bot))


class ClipMirrorCog(Cog):
    """Twitch clips channel commands"""

    def __init__(self, bot: DiscordBot):
        super().__init__()
        self.bot = bot
        self.ftp_server = ftplib.FTP()

    _PATTERNS = (
        r"((https?://)?(clips\.twitch\.tv)/[\w-]+)",
        r"((https?://)?((\w+\.)twitch\.tv)/(\w+/)?clip/[\w-]+)"
    )

    clip_channel = app_commands.Group(
            name="clips_channel",
            description="Twitch clips channel commands",
            default_permissions=Permissions(manage_channels=True),
            guild_only=True
    )

    @clip_channel.command(name="add")
    @app_commands.describe(channel="Which text channel to monitor")
    async def add_clips_channel(self, interaction: discord.Interaction, channel: TextChannel):
        """Add a channel where the bot will listen for twitch clip links"""
        channel_ids: List[int] = self.bot.config.get("CLIPS_CHANNEL_IDS")

        if channel.id in channel_ids:
            await interaction.response.send_message("Channel already added!", ephemeral=True)
            return

        channel_ids.append(channel.id)
        self.bot.config.set("CLIPS_CHANNEL_IDS", channel_ids)

        self.bot.config.save()

        await interaction.response.send_message("Channel has been added", ephemeral=True)

    @clip_channel.command(name="remove")
    @app_commands.describe(channel="Which text channel to remove monitoring from")
    async def remove_clips_channel(self, interaction: discord.Interaction, channel: TextChannel):
        """Remove channel from the monitoring list"""
        channel_ids: List[int] = self.bot.config.get("CLIPS_CHANNEL_IDS")

        if channel.id not in channel_ids:
            await interaction.response.send_message("Channel has already been removed!", ephemeral=True)
            return

        channel_ids.remove(channel.id)
        self.bot.config.set("CLIPS_CHANNEL_IDS", channel_ids)

        self.bot.config.save()

        await interaction.response.send_message("Channel has been removed", ephemeral=True)

    @remove_clips_channel.error
    @add_clips_channel.error
    async def remove_clips_channel_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(
                "You don't have the permissions to use this command!",
                ephemeral=True
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
