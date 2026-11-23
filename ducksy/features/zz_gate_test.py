import os

from discord.ext import commands


async def setup(bot: commands.Bot):
    print(os.environ)
