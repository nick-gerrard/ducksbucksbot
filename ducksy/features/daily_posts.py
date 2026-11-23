"""Today's games and open bets: /today, /bets, plus the daily posts in the main channel."""

import datetime

import discord
from discord import app_commands
from discord.ext import commands, tasks

from ducksy import ducksbucks
from ducksy.settings import CHANNEL_ID, TIMEZONE

GAMES_TIME = datetime.time(hour=10, tzinfo=TIMEZONE)  # 10am Eastern, DST-aware
BETS_TIME = datetime.time(hour=18, tzinfo=TIMEZONE)  # 6pm Eastern


class DailyPosts(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        self.daily_games.start()
        self.daily_bets.start()

    async def cog_unload(self):
        self.daily_games.cancel()
        self.daily_bets.cancel()

    async def post(self, text: str):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(CHANNEL_ID) if CHANNEL_ID else None
        if isinstance(channel, discord.abc.Messageable):
            await channel.send(text)

    @tasks.loop(time=GAMES_TIME)
    async def daily_games(self):
        await self.post(ducksbucks.format_games(await ducksbucks.todays_games()))

    @tasks.loop(time=BETS_TIME)
    async def daily_bets(self):
        await self.post(ducksbucks.format_bets(await ducksbucks.pending_bets()))

    @app_commands.command(name="today", description="Today's games")
    async def today(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(ducksbucks.format_games(await ducksbucks.todays_games()))

    @app_commands.command(name="bets", description="Get the latest DucksBucks bets!")
    async def bets(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(ducksbucks.format_bets(await ducksbucks.pending_bets()))


async def setup(bot: commands.Bot):
    await bot.add_cog(DailyPosts(bot))
