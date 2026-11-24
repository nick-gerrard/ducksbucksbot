"""/ghosthunt: call the @Ghost Hunters to don the badge and fight the paranormal.

The bot blocks role pings by default. This command lets through a ping for exactly one role,
the server's "Ghost Hunters" role, and nothing else (no @everyone, no other roles).
"""

import random
import re

import discord
from discord import app_commands
from discord.ext import commands

from ducksy.storage import Store

ROLE_NAME = "Ghost Hunters"

RALLY_CRIES = [
    "Don the badge. Grab the EMF reader. The paranormal won't fight itself. 👻",
    "Something is knocking in the walls and it owes us DucksBucks. Suit up. 🔦",
    "Ghosts don't pay rent. Time to evict them. 🏚️",
    "Salt the doorways, light the candles, and try not to scream on comms. 🕯️",
    "The spirit box is crackling. It's asking for you by name. 📻",
    "Odds of everyone surviving tonight: 12 to 1. Let's go. 💀",
    "Who you gonna call? Apparently Duck$y. Badges on. 🦆",
]


def simplify(name: str) -> str:
    """'Ghost Hunters', 'ghost-hunters' and 'GhostHunters' all become 'ghosthunters'."""
    return re.sub(r"[\s_-]", "", name).lower()


def find_role(guild: discord.Guild | None) -> discord.Role | None:
    if guild is None:
        return None
    for role in guild.roles:
        if simplify(role.name) == simplify(ROLE_NAME):
            return role
    return None


class GhostHunters(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.store = Store("ghost_hunters")

    @app_commands.command(
        name="ghosthunt", description="Call the @Ghost Hunters to fight the paranormal"
    )
    @app_commands.describe(when="When are you hunting? e.g. tonight at 9pm (optional)")
    async def ghosthunt(
        self,
        interaction: discord.Interaction,
        when: app_commands.Range[str, 1, 100] | None = None,
    ):
        role = find_role(interaction.guild)
        if role is None:
            await interaction.response.send_message(
                f"There's no `@{ROLE_NAME}` role on this server yet. Ask an admin to make one! 👻"
            )
            return
        data = self.store.load()
        data["hunts"] = data.get("hunts", 0) + 1
        self.store.save(data)
        timing = f"\n🕘 **When:** {when}" if when else ""
        await interaction.response.send_message(
            f"🚨 **GHOST HUNTERS, ASSEMBLE!** 🚨 {role.mention}\n\n"
            f"{random.choice(RALLY_CRIES)}{timing}\n"
            f"-# Called by {interaction.user.display_name}. Hunt #{data['hunts']}.",
            # Ping this one role only. Everything else stays blocked by the bot's defaults.
            allowed_mentions=discord.AllowedMentions(roles=[role]),
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(GhostHunters(bot))
