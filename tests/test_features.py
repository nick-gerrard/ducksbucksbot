"""Every feature must load, and slash commands must be valid and not clash."""

import re

import pytest

from ducksy.bot import Ducksy, feature_modules

NAME_RE = re.compile(r"^[a-z0-9_-]{1,32}$")


@pytest.fixture
async def bot():
    b = Ducksy()
    await b.load_features()
    yield b
    for name in list(b.extensions):
        await b.unload_extension(name)
    await b.close()


def test_there_are_features():
    assert "ducksy.features.basics" in feature_modules()


async def test_every_feature_loads(bot):
    assert bot.failed_features == {}
    assert set(bot.extensions) == set(feature_modules())


async def test_slash_commands_are_valid(bot):
    commands = bot.tree.get_commands()
    names = [c.name for c in commands]
    assert len(names) == len(set(names)), "two features use the same command name"
    assert len(names) <= 100, "Discord allows at most 100 slash commands"
    for c in bot.tree.walk_commands():
        assert NAME_RE.match(c.name), f"bad command name {c.name!r}"
        assert c.description and len(c.description) <= 100, f"/{c.name} needs a short description"
