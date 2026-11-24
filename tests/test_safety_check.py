"""The safety gate itself: it must pass today's features and catch the risky stuff."""

from pathlib import Path

import pytest

from scripts.safety_check import check_paths, check_source, main

ROOT = Path(__file__).resolve().parent.parent

OK_FEATURE = """
import random
import discord
from discord import app_commands
from discord.ext import commands
from ducksy.storage import Store
"""


def test_current_repo_passes():
    assert main(["--root", str(ROOT)]) == 0


def test_ok_feature():
    assert check_source("f.py", OK_FEATURE) == []


@pytest.mark.parametrize(
    "code",
    [
        "import os",
        "import subprocess",
        "from os import environ",
        "import aiohttp",
        "from pathlib import Path",
        "open('/etc/passwd')",
        "eval('1')",
        "exec('x=1')",
        "__import__('os')",
        "getattr(bot, 'tok' + 'en')",
        "bot.http.token",
        "x = bot.http",
        "().__class__.__bases__",
        "super(Foo, self).__init__.__globals__",
        "x.__init__",
        "super().__init__.__globals__",
        "discord.utils.os.system('ls')",
        "discord.File('/proc/self/environ')",
        "from discord import File",
        "await asyncio.create_subprocess_shell('ls')",
        "await guild.leave()",
        "await member.ban()",
        "await bot.close()",
        "from . import x",
        "from discord import *",
        "def f(:",
        "async def on_message(self, message): pass",
        "async def on_message_edit(self, before, after): pass",
        "await bot.wait_for('message', check=lambda m: True)",
    ],
)
def test_catches(code):
    assert check_source("f.py", code), code


@pytest.mark.parametrize(
    "code",
    [
        # any feature not on the role-ping list
        "discord.AllowedMentions(roles=[role])",
        "discord.AllowedMentions(everyone=True)",
        "discord.AllowedMentions.all()",
        "AM = discord.AllowedMentions",
        "from discord import AllowedMentions",
        "AllowedMentions(everyone=True)",
        "class M(discord.AllowedMentions): pass",
        "interaction.client.allowed_mentions = None",
        "bot.allowed_mentions.everyone",
        "role = guild.default_role",
    ],
)
def test_catches_pings(code):
    assert check_source("ducksy/features/f.py", code), code


def test_role_ping_features_may_ping_specific_roles_only():
    path = "ducksy/features/ghost_hunters.py"
    assert check_source(path, "discord.AllowedMentions(roles=[role])") == []
    assert check_source(path, "discord.AllowedMentions(roles=[a, b])") == []
    for code in [
        "discord.AllowedMentions(everyone=True)",
        "discord.AllowedMentions(roles=True)",
        "discord.AllowedMentions(roles=guild.roles)",
        "discord.AllowedMentions(roles=[*guild.roles])",
        "discord.AllowedMentions(roles=[r for r in guild.roles])",
        "discord.AllowedMentions(roles=[])",
        "discord.AllowedMentions(roles=[role], everyone=True)",
        "discord.AllowedMentions(roles=[role], users=True)",
        "discord.AllowedMentions(**opts)",
        "discord.AllowedMentions.all()",
        "AM = discord.AllowedMentions",
    ]:
        assert check_source(path, code), code


def test_paths():
    assert check_paths(["ducksy/features/new.py", "tests/features/test_new.py"]) == []
    assert check_paths(["ducksy/bot.py"])
    assert check_paths(["pyproject.toml"])
    assert check_paths([".github/workflows/ci.yml"])
    assert check_paths(["ducksy/features/sub/x.py"])
    assert check_paths(["ducksy/features/data.json"])


def test_owner_skips_path_rule(tmp_path):
    changed = tmp_path / "changed.txt"
    changed.write_text("ducksy/bot.py\n")
    assert main(["--root", str(ROOT), "--changed-files", str(changed)]) == 1
    assert main(["--root", str(ROOT), "--changed-files", str(changed), "--owner"]) == 0


@pytest.mark.parametrize("code", ["from ducksy import bot", "from ducksy import __main__"])
def test_ducksy_core_is_off_limits(code):
    assert check_source("f.py", code)


def test_super_init_is_allowed():
    assert (
        check_source(
            "f.py", "class V:\n    def __init__(self):\n        super().__init__(timeout=1)\n"
        )
        == []
    )
