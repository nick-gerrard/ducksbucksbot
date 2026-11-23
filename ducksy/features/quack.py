"""/quack and /coinflip: a small example feature that remembers things between restarts.

Copy this file when starting a new feature.
"""

import random

import discord
from discord import app_commands
from discord.ext import commands

from ducksy.storage import Store

QUACKS = ["Quack!", "QUACK!!", "quack?", "Quaaaaack.", "*aggressive quacking*"]


class Quack(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.store = Store("quack")

    @app_commands.command(name="quack", description="Duck$y quacks and keeps count")
    async def quack(self, interaction: discord.Interaction):
        data = self.store.load()
        data["total"] = data.get("total", 0) + 1
        self.store.save(data)
        await interaction.response.send_message(f"{random.choice(QUACKS)} (quack #{data['total']})")

    @app_commands.command(name="coinflip", description="Heads or tails, for settling disputes")
    async def coinflip(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"🪙 {random.choice(['Heads', 'Tails'])}!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Quack(bot))
