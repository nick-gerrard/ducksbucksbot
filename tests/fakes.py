"""Stand-ins for Discord objects, so feature tests can call slash commands without Discord.

    from tests.fakes import FakeInteraction, call

    async def test_quack():
        cog = Quack(bot=None)
        i = FakeInteraction()
        await call(cog.quack, i)
        assert "Quack" in i.text

`call(command, interaction, *options)` runs a slash command method the way Discord would.
After it runs, `i.text` is the last thing Duck$y said, `i.sent` lists every message (with
their `embed`, `view`, `ephemeral`, ...), and `i.deferred` says whether it called `defer()`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FakeUser:
    id: int = 1234
    name: str = "testduck"
    display_name: str = "Test Duck"
    bot: bool = False

    @property
    def mention(self) -> str:
        return f"<@{self.id}>"

    def __str__(self) -> str:
        return self.name


@dataclass
class Sent:
    content: str | None
    kwargs: dict[str, Any]

    def __getattr__(self, name: str) -> Any:  # sent.embed, sent.view, sent.ephemeral
        return self.kwargs.get(name)


class _Response:
    def __init__(self, interaction: FakeInteraction):
        self._i = interaction
        self._done = False

    def is_done(self) -> bool:
        return self._done

    async def send_message(self, content: str | None = None, **kwargs: Any) -> None:
        assert not self._done, "replied twice: use interaction.followup.send for the second message"
        self._done = True
        self._i.sent.append(Sent(content, kwargs))

    async def defer(self, **kwargs: Any) -> None:
        assert not self._done, "defer() must come before any reply"
        self._done = True
        self._i.deferred = True

    async def edit_message(self, content: str | None = None, **kwargs: Any) -> None:
        self._done = True
        self._i.sent.append(Sent(content, kwargs))


class _Followup:
    def __init__(self, interaction: FakeInteraction):
        self._i = interaction

    async def send(self, content: str | None = None, **kwargs: Any) -> None:
        assert self._i.response.is_done(), "followup.send needs defer() or a reply first"
        self._i.sent.append(Sent(content, kwargs))


@dataclass
class FakeInteraction:
    user: FakeUser = field(default_factory=FakeUser)
    channel_id: int = 42
    guild_id: int = 99
    sent: list[Sent] = field(default_factory=list)
    deferred: bool = False

    def __post_init__(self) -> None:
        self.response = _Response(self)
        self.followup = _Followup(self)

    @property
    def text(self) -> str:
        """The last message's text ('' if none)."""
        return (self.sent[-1].content or "") if self.sent else ""


async def call(command: Any, interaction: FakeInteraction, *args: Any, **kwargs: Any) -> None:
    """Run a slash command (e.g. `cog.quack`) with a fake interaction and its options."""
    await command.callback(command.binding, interaction, *args, **kwargs)
