"""Tests for /magic8."""

from ducksy.features.magic8 import ANSWERS, Magic8


class FakeResponse:
    def __init__(self):
        self.sent = []

    async def send_message(self, text):
        self.sent.append(text)


class FakeInteraction:
    def __init__(self):
        self.response = FakeResponse()


async def test_magic8_answers_and_counts():
    cog = Magic8(bot=None)  # type: ignore[arg-type]
    first = FakeInteraction()
    await cog.magic8.callback(cog, first, "Will the Ducks win?")  # type: ignore[arg-type]
    second = FakeInteraction()
    await cog.magic8.callback(cog, second, "Should I bet it all?")  # type: ignore[arg-type]

    text = first.response.sent[0]
    assert "Will the Ducks win?" in text
    assert any(answer in text for answer in ANSWERS)
    assert "Question #1 " in text
    assert "Question #2 " in second.response.sent[0]
    assert cog.store.load()["asked"] == 2
