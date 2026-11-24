"""Tests for /call."""

from dataclasses import dataclass

import discord
import pytest

from ducksy.features.call import Call
from ducksy.media import media_dir
from tests.fakes import FakeInteraction, call


@dataclass
class FakeRole:
    id: int
    name: str

    @property
    def mention(self) -> str:
        return f"<@&{self.id}>"


@dataclass
class FakeGuild:
    roles: list[FakeRole]


async def test_no_role_on_server():
    cog = Call(bot=None)  # type: ignore[arg-type]
    i = FakeInteraction()
    i.guild = FakeGuild(roles=[FakeRole(1, "everyone")])  # type: ignore[attr-defined]
    await call(cog.call, i)
    assert "no `@Apostates` role" in i.text
    assert i.sent[-1].ephemeral is True


@pytest.mark.parametrize("name", ["Apostates", "apostates", "a-postates", "A_postates"])
async def test_role_name_variants(name):
    cog = Call(bot=None)  # type: ignore[arg-type]
    i = FakeInteraction()
    i.guild = FakeGuild(roles=[FakeRole(7, name)])  # type: ignore[attr-defined]
    await call(cog.call, i)
    assert "<@&7>" in i.text


async def test_pings_only_apostates_with_and_without_when():
    cog = Call(bot=None)  # type: ignore[arg-type]
    apostates = FakeRole(555, "Apostates")
    i = FakeInteraction()
    i.guild = FakeGuild(roles=[FakeRole(1, "everyone"), apostates])  # type: ignore[attr-defined]
    await call(cog.call, i, "9pm")

    assert "📞 **Friday night call!** <@&555>" in i.text
    assert "\nWhen: 9pm" in i.text
    assert "file" not in i.sent[-1].kwargs
    allowed = i.sent[-1].allowed_mentions
    assert allowed.roles == [apostates]
    assert allowed.everyone is not True  # left to the bot's default (blocked)

    i2 = FakeInteraction()
    i2.guild = FakeGuild(roles=[apostates])  # type: ignore[attr-defined]
    await call(cog.call, i2)
    assert i2.text == "📞 **Friday night call!** <@&555>"
    assert "When:" not in i2.text
    assert "file" not in i2.sent[-1].kwargs


async def test_attaches_random_image_when_available():
    (media_dir("call") / "meme.png").write_bytes(b"\x89PNG")
    cog = Call(bot=None)  # type: ignore[arg-type]
    apostates = FakeRole(555, "Apostates")
    i = FakeInteraction()
    i.guild = FakeGuild(roles=[apostates])  # type: ignore[attr-defined]
    await call(cog.call, i)

    assert "<@&555>" in i.text
    attached = i.sent[-1].file
    assert isinstance(attached, discord.File)
    try:
        assert attached.filename == "meme.png"
    finally:
        attached.close()
    allowed = i.sent[-1].allowed_mentions
    assert allowed.roles == [apostates]
    assert allowed.everyone is not True
