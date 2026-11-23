"""Duck$y's basic commands: /ping, /intro, /gamblers."""

import discord
from discord import app_commands
from discord.ext import commands


class Basics(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")

    @app_commands.command(name="intro", description="Hi Duck$y")
    async def intro(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Hi! I'm Duck$y, the official mascot of DucksBucks, "
            "and I'm here to assist with all your gambling needs!"
        )

    @app_commands.command(name="gamblers", description="Rally the gamblers")
    async def gamblers(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hi @gamblers! Ready to learn about bets?")


async def setup(bot: commands.Bot):
    await bot.add_cog(Basics(bot))
