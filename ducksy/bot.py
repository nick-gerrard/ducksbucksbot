"""The bot core: loads every feature in ducksy/features/ and keeps the bot safe to run."""

import logging
import pkgutil

import discord
from discord import app_commands
from discord.ext import commands

import ducksy.features

log = logging.getLogger("ducksy")


def feature_modules() -> list[str]:
    """Every module in ducksy/features/, except ones starting with `_`."""
    return sorted(
        f"ducksy.features.{m.name}"
        for m in pkgutil.iter_modules(ducksy.features.__path__)
        if not m.name.startswith("_")
    )


class Ducksy(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=discord.Intents.default(),
            # Never mass-ping: no @everyone/@here or role pings, whatever a feature sends.
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True),
        )
        self.failed_features: dict[str, str] = {}

    async def load_features(self) -> None:
        for name in feature_modules():
            try:
                await self.load_extension(name)
                log.info("loaded feature %s", name)
            except Exception as e:  # one broken feature shouldn't take the whole bot down
                log.exception("feature %s failed to load", name)
                self.failed_features[name] = repr(e)

    async def setup_hook(self) -> None:
        self.tree.on_error = self.on_app_command_error
        await self.load_features()
        synced = await self.tree.sync()
        log.info("synced %d slash commands", len(synced))

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        log.error(
            "command %s failed", interaction.command and interaction.command.name, exc_info=error
        )
        msg = "Quack! Something went wrong with that command. 🦆💥"
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)
