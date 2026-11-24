"""/ghosthunt: call the ghost hunters to don the badge and fight the paranormal.

Discord role pings are blocked for the bot, so ghost hunters sign up with /ghosthunt_join
and Duck$y pings each of them by name instead.
"""

import random

import discord
from discord import app_commands
from discord.ext import commands

from ducksy.storage import Store

RALLY_CRIES = [
    "Don the badge. Grab the EMF reader. The paranormal won't fight itself. 👻",
    "Something is knocking in the walls and it owes us DucksBucks. Suit up. 🔦",
    "Ghosts don't pay rent. Time to evict them. 🏚️",
    "Salt the doorways, light the candles, and try not to scream on comms. 🕯️",
    "The spirit box is crackling. It's asking for you by name. 📻",
    "Odds of everyone surviving tonight: 12 to 1. Let's go. 💀",
    "Who you gonna call? Apparently Duck$y. Badges on. 🦆",
]


class GhostHunters(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.store = Store("ghost_hunters")

    def hunters(self) -> list[str]:
        return self.store.load().get("hunters", [])

    def save_hunters(self, hunters: list[str]) -> None:
        data = self.store.load()
        data["hunters"] = hunters
        self.store.save(data)

    @app_commands.command(
        name="ghosthunt", description="Call the ghost hunters to fight the paranormal"
    )
    @app_commands.describe(when="When are you hunting? e.g. tonight at 9pm (optional)")
    async def ghosthunt(
        self,
        interaction: discord.Interaction,
        when: app_commands.Range[str, 1, 100] | None = None,
    ):
        hunters = self.hunters()
        if not hunters:
            await interaction.response.send_message(
                "No ghost hunters yet! Sign up with `/ghosthunt_join` first. 👻"
            )
            return
        data = self.store.load()
        data["hunts"] = data.get("hunts", 0) + 1
        self.store.save(data)
        pings = " ".join(f"<@{hunter}>" for hunter in hunters)
        timing = f"\n🕘 **When:** {when}" if when else ""
        await interaction.response.send_message(
            f"🚨 **GHOST HUNTERS, ASSEMBLE!** 🚨\n{pings}\n\n"
            f"{random.choice(RALLY_CRIES)}{timing}\n"
            f"-# Called by {interaction.user.display_name}. Hunt #{data['hunts']}."
        )

    @app_commands.command(name="ghosthunt_join", description="Join the ghost hunters")
    async def ghosthunt_join(self, interaction: discord.Interaction):
        hunters = self.hunters()
        me = str(interaction.user.id)
        if me in hunters:
            await interaction.response.send_message("You're already a ghost hunter. 🪪")
            return
        hunters.append(me)
        self.save_hunters(hunters)
        await interaction.response.send_message(
            f"{interaction.user.mention} has joined the ghost hunters! Badge issued. 🪪👻"
        )

    @app_commands.command(name="ghosthunt_leave", description="Hand in your ghost hunter badge")
    async def ghosthunt_leave(self, interaction: discord.Interaction):
        hunters = self.hunters()
        me = str(interaction.user.id)
        if me not in hunters:
            await interaction.response.send_message("You weren't a ghost hunter anyway. 🤷")
            return
        hunters.remove(me)
        self.save_hunters(hunters)
        await interaction.response.send_message(
            f"{interaction.user.display_name} handed in their badge. The ghosts thank you. 👻"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(GhostHunters(bot))
