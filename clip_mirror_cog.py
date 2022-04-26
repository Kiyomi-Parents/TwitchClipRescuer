from pathlib import Path
from typing import List

import discord
from discord import Message, PartialEmoji, app_commands, TextChannel
from discord.app_commands import MissingPermissions
from discord.ext import commands
from discord.ext.commands import Cog

import downloader
import ftp

from main import DiscordBot
from platforms import Platform, _get_platform


async def setup(bot: DiscordBot):
    await bot.add_cog(ClipMirrorCog(bot))


class ClipMirrorCog(Cog, app_commands.Group, name="clips_channel"):
    """Twitch clips channel commands"""

    def __init__(self, bot: DiscordBot):
        super().__init__()
        self.bot = bot

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="add")
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

    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.command(name="remove")
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

        try:
            platform, url = _get_platform(message.content)
        except TypeError:
            return

        if platform == Platform.Unknown and not self.bot.config.get("ALLOW_UNKNOWN_SOURCES"):
            return

        kwargs = {}

        if "FTP" in self.bot.config.get("ENABLED_MODES"):
            ftp_settings = self.bot.config.get("FTP")
            kwargs["ftp_server"] = ftp.FTP(
                host=ftp_settings["HOST"],
                port=ftp_settings["PORT"],
                username=ftp_settings["USERNAME"],
                password=ftp_settings["PASSWORD"],
                sub_directory=Path(ftp_settings["SUBDIRECTORY"])
            )

        kwargs["delete_local"] = "LOCAL" not in self.bot.config.get("ENABLED_MODES")

        target_directory = Path(self.bot.config.get("PATH"))
        if self.bot.config.get("CREATE_DISCORD_CHANNEL_SUBDIRECTORY"):
            target_directory /= Path(message.channel.name)
        if self.bot.config.get("CREATE_PLATFORM_SUBDIRECTORY"):
            target_directory /= Path(platform.name)
        output_template = self.bot.config.get("OUTPUT_TEMPLATE")

        try:
            downloader.download_clip(url, output_template, target_directory, **kwargs)
        except Exception as e:
            await message.add_reaction("❌")
            raise e

        await message.add_reaction(PartialEmoji(name="✅"))
