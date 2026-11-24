"""/call: call the @Apostates to the Friday night call with a random meme.

The bot blocks role pings by default. This command lets through a ping for exactly one role,
the server's "Apostates" role, and nothing else (no @everyone, no other roles).
"""

import re

import discord
from discord import app_commands
from discord.ext import commands

from ducksy.media import random_image

ROLE_NAME = "Apostates"


def simplify(name: str) -> str:
    """'Apostates', 'apostates' and 'a-postates' all become 'apostates'."""
    return re.sub(r"[\s_-]", "", name).lower()


def find_role(guild: discord.Guild | None) -> discord.Role | None:
    if guild is None:
        return None
    for role in guild.roles:
        if simplify(role.name) == simplify(ROLE_NAME):
            return role
    return None


class Call(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="call", description="Call the Apostates to the Friday night call")
    @app_commands.describe(when="When the call is, e.g. 9pm or 'right now'")
    async def call(self, interaction: discord.Interaction, when: str | None = None):
        role = find_role(interaction.guild)
        if role is None:
            await interaction.response.send_message(
                f"There's no `@{ROLE_NAME}` role on this server yet. Ask an admin to make one.",
                ephemeral=True,
            )
            return

        content = f"📞 **Friday night call!** {role.mention}"
        if when:
            content += f"\nWhen: {when}"

        file = random_image("call")
        if file is not None:
            await interaction.response.send_message(
                content,
                file=file,
                # Ping this one role only. Everything else stays blocked by the bot's defaults.
                allowed_mentions=discord.AllowedMentions(roles=[role]),
            )
        else:
            await interaction.response.send_message(
                content,
                # Ping this one role only. Everything else stays blocked by the bot's defaults.
                allowed_mentions=discord.AllowedMentions(roles=[role]),
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Call(bot))
