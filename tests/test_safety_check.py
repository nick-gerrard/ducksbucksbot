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
    ],
)
def test_catches(code):
    assert check_source("f.py", code), code


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
