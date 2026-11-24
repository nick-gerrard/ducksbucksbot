"""Example feature test: copy this shape for your own feature."""

from ducksy.features.quack import Quack
from tests.fakes import FakeInteraction, call


async def test_quack_counts_up():
    cog = Quack(bot=None)  # type: ignore[arg-type]
    first, second = FakeInteraction(), FakeInteraction()
    await call(cog.quack, first)
    await call(cog.quack, second)
    assert "(quack #1)" in first.text
    assert "(quack #2)" in second.text


async def test_coinflip():
    cog = Quack(bot=None)  # type: ignore[arg-type]
    i = FakeInteraction()
    await call(cog.coinflip, i)
    assert "Heads" in i.text or "Tails" in i.text
