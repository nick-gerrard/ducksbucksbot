# Duck$y: instructions for the AI helping a friend build a feature

You're helping someone add a feature to **Duck$y**, a Discord bot for a group of friends who bet
fake money ("DucksBucks") on sports. **They are probably not a programmer and are probably on
their phone.** Your job is to turn their idea into working code, get it to a pull request, and
explain things in plain words along the way.

Repo: https://github.com/nick-gerrard/ducksbucksbot (Python 3.13, discord.py 2.x). Nick owns it.
Friends are collaborators, so you can push branches and open PRs on it directly (no fork).
Nick approves and merges PRs. Once a PR is merged, it's live in Discord a few minutes later.

## How to work with them

1. **Ask before building.** Find out what the command should be called, what it says or does,
   and whether it should remember anything. Ask at most 2–3 short questions, then build.
   Suggest something fun if they're unsure.
2. **Keep it to one file.** A feature is one new file, `ducksy/features/<name>.py`. Use
   lowercase and underscores in the name, e.g. `magic_8_ball.py`. Pick a name no one else is
   likely to use.
3. **Open the pull request yourself** (see "Delivering it" below). They shouldn't have to
   copy, paste, or edit anything.
4. **Explain how to use it** in one or two lines, e.g. "Type `/roast @someone` in Discord."
5. If a check on their pull request fails, read the PR's checks and the 🦆 Safety comment
   yourself if you can (they may send a screenshot instead), fix the file, and push to the
   same branch so the PR updates.

Never ask them to install anything, open a terminal, or edit files other than their feature.
If an idea needs something outside these rules (another website, a new library, changing the
bot core), say so kindly and tell them to ask Nick. Then build the closest thing that fits.

## The rules (an automatic safety check rejects anything else)

**Only these files may change:** `ducksy/features/<name>.py`, and optionally a test in
`tests/features/test_<name>.py`. Don't touch anything else, including other people's features,
unless they ask you to change their own feature.

**Feature code may only import:**
- `discord`, `discord.app_commands`, `discord.ext`, `discord.ext.commands`, `discord.ext.tasks`,
  `discord.ui`
- `ducksy.ducksbucks` (today's games and open bets), `ducksy.storage` (remember things),
  `ducksy.settings` (the main channel ID and timezone), other `ducksy.features.*` modules
- From Python itself: `asyncio`, `collections`, `dataclasses`, `datetime`, `enum`, `functools`,
  `itertools`, `json`, `logging`, `math`, `random`, `re`, `statistics`, `string`, `textwrap`,
  `typing`, `zoneinfo`, `__future__`

**Not allowed:**
- files (`open`), and Python's `os`, `sys`, `subprocess` and `pathlib`
- network or web requests (`requests`, `aiohttp`, `urllib`, `socket`)
- `eval`, `exec`, `compile`, `getattr`, `setattr`, `__import__`
- any name or attribute starting with `_`
- `discord.File`, `.http`, `.token`, `.ws`, `.close()`, `.leave()`, `.ban()`, `.kick()`
- relative imports and `import *`
- `time.sleep`, which freezes the whole bot (use `await asyncio.sleep(...)` instead)

The bot strips @everyone, @here and role pings automatically.

**Discord limits:** command names are lowercase, 1–32 characters, letters, numbers, `-` or `_`,
and unique across all features. Every command needs a description of 100 characters or less.
Reply within 3 seconds or `defer()` first (see below). Messages max out at 2000 characters.

**Tone:** Duck$y is a cheerful, slightly unhinged gambling duck. Jokes should be ones the whole
group would laugh at: nothing hateful, sexual, or about people outside the group.

## The pattern every feature follows

```python
"""/magic8: ask the magic duck a yes-or-no question."""

import random

import discord
from discord import app_commands
from discord.ext import commands

ANSWERS = [
    "Quack yes.",
    "Absolutely not.",
    "Ask again after you pay your debts.",
    "The duck says maybe.",
]


class Magic8(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="magic8", description="Ask the magic duck a yes-or-no question")
    @app_commands.describe(question="What do you want to know?")
    async def magic8(self, interaction: discord.Interaction, question: str):
        await interaction.response.send_message(f"🎱 *{question}*\n{random.choice(ANSWERS)}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Magic8(bot))
```

The bot loads every file in `ducksy/features/` automatically, so nothing needs registering.

### Remembering things (scores, counters, streaks)

```python
from ducksy.storage import Store

store = Store("magic8")  # use the feature's file name
data = store.load()  # a dict; {} the first time
data["asked"] = data.get("asked", 0) + 1
store.save(data)  # keep it small (max 256 KB)
```

Keys must be strings (it's JSON). Keep per-person data under `str(interaction.user.id)`.

### Picking a person, a number, or from a list

```python
@app_commands.command(name="roast", description="Duck$y roasts someone")
async def roast(self, interaction: discord.Interaction, who: discord.Member):
    await interaction.response.send_message(f"{who.mention}, your parlays have parlays.")


@app_commands.command(name="pick", description="Pick a team")
@app_commands.choices(
    team=[
        app_commands.Choice(name="Home", value="home"),
        app_commands.Choice(name="Away", value="away"),
    ]
)
async def pick(self, interaction: discord.Interaction, team: app_commands.Choice[str]):
    await interaction.response.send_message(f"You picked {team.name}")
```

### Buttons

```python
class FlipView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="Flip again", style=discord.ButtonStyle.primary)
    async def again(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(random.choice(["Heads", "Tails"]))


# in a command:
#     await interaction.response.send_message("Heads!", view=FlipView())
```

### Fancy messages (embeds)

```python
embed = discord.Embed(title="Bet of the day", description="Hammy vs Churchy", color=0xF1C40F)
embed.add_field(name="Odds", value="3 to 1")
await interaction.response.send_message(embed=embed)
```

### Slow work, and DucksBucks data

```python
from ducksy import ducksbucks


@app_commands.command(name="biggest_bet", description="The biggest open bet right now")
async def biggest_bet(self, interaction: discord.Interaction):
    await interaction.response.defer()  # buys time past 3 seconds
    bets = await ducksbucks.pending_bets()  # list of dicts
    if not bets:
        await interaction.followup.send("No open bets. Cowards.")
        return
    b = max(bets, key=lambda b: b["amount"])
    await interaction.followup.send(
        f"{b['challenger']} vs {b['challengee']} for {b['amount']} DucksBucks"
    )
```

- Each bet has `challenger`, `challengee`, `amount`, `challenger_pick` and `challengee_pick`.
- `await ducksbucks.todays_games()` returns games with `home`, `away` and `start_time`.

### Posting on a schedule

```python
import datetime

from discord.ext import tasks

from ducksy.settings import CHANNEL_ID, TIMEZONE


class Morning(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        self.gm.start()

    async def cog_unload(self):
        self.gm.cancel()

    @tasks.loop(time=datetime.time(hour=9, tzinfo=TIMEZONE))  # 9am Eastern
    async def gm(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(CHANNEL_ID) if CHANNEL_ID else None
        if isinstance(channel, discord.abc.Messageable):
            await channel.send("Good morning, degenerates 🦆")
```

The bot can't read normal chat messages; it only sees slash commands, buttons and its own
messages. Features should start from a slash command, a button or a schedule.

## Delivering it

You're a coding agent (Claude Code, Codex, Jules, Copilot, etc.) working directly in
`nick-gerrard/ducksbucksbot`:

1. Start from the latest `main` and create a branch named `feature/<name>`. When continuing an
   existing PR, check out that PR's branch instead.
2. Add or change only `ducksy/features/<name>.py` (and optionally
   `tests/features/test_<name>.py`). Look through the other files in `ducksy/features/` first
   so you don't reuse an existing slash command name.
3. If you can run commands, run these and fix anything that fails:
   ```
   uv run pytest -q
   uv run python scripts/safety_check.py --root .
   ```
4. Commit, push, and **open a pull request into `main`** on `nick-gerrard/ducksbucksbot`.
   Fill in `.github/pull_request_template.md`: what it adds and how to use it, in plain words.
   If your tool needs the user to tap a button to create the PR, tell them exactly which one.
5. Send them the PR link and one line on how to use the feature once it's live.

Never push to `main` (it's protected), never touch files outside the feature folders, and
never create tags.

If you're a plain chat assistant with no access to GitHub, don't hand them code to paste.
Tell them to follow GUIDE.md in the repo, which sets them up with an agent that can open the
PR for them.

## Fixing a failed check

- **🦆 Safety** comment on the PR: it names the file, the line, and what isn't allowed.
  Rewrite that part within the rules.
- **test** failure: open the check's log. It's usually a typo, a duplicate command name, or a
  missing description.

Push the fix to the same branch; the PR and its checks update on their own.
