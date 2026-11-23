# Duck$y: notes for AI assistants

Duck$y is a discord.py 2.x bot (Python 3.13, uv). Most contributors are non-developers working
through an AI assistant, so keep changes small, explain them simply, and follow these rules.
A safety check (`scripts/safety_check.py`) enforces them on every PR, and a PR that breaks them
won't be merged.

## Where changes go

- A new feature is **one new file** in `ducksy/features/<feature_name>.py` (lowercase, underscores).
  `ducksy/bot.py` loads every file in that folder automatically; don't register it anywhere.
- Copy the shape of `ducksy/features/quack.py`: a `commands.Cog` subclass with
  `@app_commands.command(...)` methods, and `async def setup(bot)` that calls `bot.add_cog(...)`.
- Optional tests go in `tests/features/test_<feature_name>.py` (pytest, asyncio_mode=auto).
- Do **not** edit anything outside `ducksy/features/` and `tests/features/`: not the core,
  `pyproject.toml`, `uv.lock`, workflows, `deploy.toml`, or the docs. If the feature truly needs
  a core change or a new dependency, stop and tell the user to ask Nick instead.
- Don't edit or delete other people's features unless the user asks for exactly that.

## What feature code may use

- Imports only from: `discord` (incl. `discord.app_commands`, `discord.ext.commands`,
  `discord.ext.tasks`, `discord.ui`), `ducksy.ducksbucks`, `ducksy.storage`, `ducksy.settings`,
  other `ducksy.features.*` modules, and the stdlib modules `asyncio`, `collections`,
  `dataclasses`, `datetime`, `enum`, `functools`, `itertools`, `json`, `logging`, `math`,
  `random`, `re`, `statistics`, `string`, `textwrap`, `typing`, `zoneinfo`, `__future__`.
- To remember things, use `ducksy.storage.Store("<name>")` (`.load()` → dict, `.save(dict)`).
  Use the feature's file name as the store name. Keep stored data small (≤256 KB).
- For DucksBucks data: `await ducksbucks.todays_games()`, `await ducksbucks.pending_bets()`.
- Scheduled posts: `tasks.loop(time=datetime.time(hour=..., tzinfo=settings.TIMEZONE))`,
  started in `cog_load` and cancelled in `cog_unload`; post to `settings.CHANNEL_ID`
  (see `daily_posts.py`).

Not allowed (the check rejects them): `open`, `eval`/`exec`/`compile`, `getattr`/`setattr`,
`__import__`, any attribute starting with `_`, `os`/`sys`/`subprocess`/`pathlib`/network
modules, `discord.File`, `.http`, `.token`, `.ws`, `.close`, `.leave`, `.ban`, `.kick`,
`asyncio` subprocess/socket helpers, relative imports, `import *`. Never use `time.sleep`
(it freezes the bot); use `await asyncio.sleep(...)`.

## Slash command rules

- Names: lowercase, 1–32 chars, letters/numbers/`-`/`_`, unique across all features
  (check the other files in `ducksy/features/`). Every command needs a description ≤100 chars.
- Reply within 3 seconds or call `await interaction.response.defer()` first and then
  `await interaction.followup.send(...)`.
- Messages are capped at 2000 characters.

## Before opening a PR

Run all of these and fix what fails:

```bash
uv run ruff format .
uv run ruff check .
uv run pyright
uv run pytest
uv run python scripts/safety_check.py --root .
```

Then open the PR against `nick-gerrard/ducksbucksbot` `main` using the PR template, and describe
the new command(s) in plain words.

## Tone

Duck$y is a cheerful, slightly unhinged gambling duck. Fun is the point. Keep jokes the kind
the whole group would laugh at: nothing hateful, sexual, or about people outside the group.
