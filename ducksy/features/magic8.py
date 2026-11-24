"""/magic8: ask the magic duck a yes-or-no question and get a gambling-themed answer."""

import random

import discord
from discord import app_commands
from discord.ext import commands

from ducksy.storage import Store

ANSWERS = [
    # yes
    "Lock it in. Max bet. 🔒",
    "The odds are in your favor, degenerate.",
    "Quack yes. Bet the house.",
    "Signs point to a fat payout. 💰",
    "That's a guaranteed parlay leg. (It is not, but yes.)",
    "The duck has run the numbers: YES.",
    # maybe
    "Push. Ask again after the next game.",
    "The line hasn't moved yet. Check back later.",
    "Too close to call. Hedge your bets.",
    "Reply hazy. The duck is counting cards.",
    # no
    "Fade it. Hard.",
    "The house says no. The house always wins.",
    "Absolutely not. Ask again after you pay your debts.",
    "That's a bad beat waiting to happen.",
    "The duck would not put a single DucksBuck on that.",
    "Odds are long. Like, really long. No.",
]


class Magic8(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.store = Store("magic8")

    @app_commands.command(name="magic8", description="Ask the magic duck a yes-or-no question")
    @app_commands.describe(question="What do you want to know?")
    async def magic8(
        self, interaction: discord.Interaction, question: app_commands.Range[str, 1, 300]
    ):
        data = self.store.load()
        data["asked"] = data.get("asked", 0) + 1
        self.store.save(data)
        await interaction.response.send_message(
            f"🎱 *{question}*\n**{random.choice(ANSWERS)}**\n"
            f"-# Question #{data['asked']} for the magic duck."
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Magic8(bot))
