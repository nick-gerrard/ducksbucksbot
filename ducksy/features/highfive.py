"""/highfive: send a random high-five GIF to the channel. """

import random

import discord
from discord import app_commands
from discord.ext import commands


HIGH_FIVE_GIFS = [
    "https://media.giphy.com/media/3ornjLd54l3eQYmfpC/giphy.gif",
    "https://media.giphy.com/media/MY7FJ58qgSZcWpvMjH/giphy.gif",
    "https://media.giphy.com/media/nkJ86JbtpRGd6ovMSX/giphy.gif",
    "https://media.giphy.com/media/YmthfXmtS80uEU5ccs/giphy.gif",
    "https://media.giphy.com/media/KgF7QNrRkGB2Ha4upn/giphy.gif",
]

HIGH_FIVE_MESSAGES = [
    "SLAP! That's teamwork. 🖐️",
    "A high five for the books! 🙌",
    "Quack yeah! Nice one. 🦆🖐️",
    "Up top! You earned it. ✋",
]


class Highfive(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="highfive", description="Give the channel a high five")
    async def highfive(self, interaction: discord.Interaction):
        embed = discord.Embed(description=random.choice(HIGH_FIVE_MESSAGES))
        embed.set_image(url=random.choice(HIGH_FIVE_GIFS))
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Highfive(bot))
