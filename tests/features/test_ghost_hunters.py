"""Tests for /ghosthunt."""

from dataclasses import dataclass

from ducksy.features.ghost_hunters import GhostHunters
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
    cog = GhostHunters(bot=None)  # type: ignore[arg-type]
    i = FakeInteraction()
    i.guild = FakeGuild(roles=[FakeRole(1, "everyone")])  # type: ignore[attr-defined]
    await call(cog.ghosthunt, i)
    assert "no `@ghosthunters` role" in i.text


async def test_pings_only_the_ghosthunters_role():
    cog = GhostHunters(bot=None)  # type: ignore[arg-type]
    hunters = FakeRole(555, "GhostHunters")
    i = FakeInteraction()
    i.guild = FakeGuild(roles=[FakeRole(1, "everyone"), hunters])  # type: ignore[attr-defined]
    await call(cog.ghosthunt, i, "tonight at 9pm")

    assert "<@&555>" in i.text
    assert "tonight at 9pm" in i.text
    assert "Hunt #1" in i.text
    allowed = i.sent[-1].allowed_mentions
    assert allowed.roles == [hunters]
    assert allowed.everyone is not True  # left to the bot's default (blocked)

    i2 = FakeInteraction()
    i2.guild = FakeGuild(roles=[hunters])  # type: ignore[attr-defined]
    await call(cog.ghosthunt, i2)
    assert "When" not in i2.text
    assert "Hunt #2" in i2.text
