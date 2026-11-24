"""Tests for /ghosthunt."""

from ducksy.features.ghost_hunters import GhostHunters


class FakeResponse:
    def __init__(self):
        self.sent = []

    async def send_message(self, text):
        self.sent.append(text)


class FakeUser:
    def __init__(self, user_id, name):
        self.id = user_id
        self.display_name = name
        self.mention = f"<@{user_id}>"


class FakeInteraction:
    def __init__(self, user):
        self.user = user
        self.response = FakeResponse()


ALICE = FakeUser(111, "Alice")
BOB = FakeUser(222, "Bob")


async def run(command, cog, user, *args):
    interaction = FakeInteraction(user)
    await command.callback(cog, interaction, *args)
    return interaction.response.sent[0]


async def test_no_hunters_yet():
    cog = GhostHunters(bot=None)  # type: ignore[arg-type]
    text = await run(cog.ghosthunt, cog, ALICE, None)
    assert "ghosthunt_join" in text


async def test_join_call_and_leave():
    cog = GhostHunters(bot=None)  # type: ignore[arg-type]
    await run(cog.ghosthunt_join, cog, ALICE)
    await run(cog.ghosthunt_join, cog, BOB)
    assert "already" in await run(cog.ghosthunt_join, cog, ALICE)

    text = await run(cog.ghosthunt, cog, ALICE, "tonight at 9pm")
    assert "<@111>" in text and "<@222>" in text
    assert "tonight at 9pm" in text
    assert "Hunt #1" in text

    await run(cog.ghosthunt_leave, cog, BOB)
    text = await run(cog.ghosthunt, cog, ALICE, None)
    assert "<@222>" not in text
    assert "When" not in text
    assert "Hunt #2" in text
