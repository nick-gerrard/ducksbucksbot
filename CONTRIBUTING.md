# Adding a feature to Duck$y

You don't need to know how to code. You need a GitHub account, an AI coding assistant (Claude
Code works great; others are fine), and an idea.

## The short version

1. **Fork** this repo on GitHub (the "Fork" button, top right), then clone your fork.
2. Open your AI assistant in the folder and tell it what you want, for example:
   > Add a Duck$y feature: a /roast command that picks a random roast for the person you choose.
   > Follow CLAUDE.md.
3. Ask it to run the checks: `uv run pytest`.
4. Ask it to commit, push, and **open a pull request** against `nick-gerrard/ducksbucksbot`.
5. Wait for the checks. If the 🦆 **Safety check** comments with problems, paste the comment
   into your AI and ask it to fix them, then push again.
6. Nick merges it, and a few minutes later it's live in Discord.

## The rules (the safety check enforces these)

- **One feature, one file**, in `ducksy/features/`. Tests can go in `tests/features/`.
  Changing anything else (the bot core, dependencies, the deploy setup) needs Nick, so ask him.
- **Features can use:** Discord (`discord`, slash commands, buttons, embeds, scheduled tasks),
  randomness, dates and times, math, text, JSON, `asyncio.sleep`, the DucksBucks data
  (`ducksy.ducksbucks`), and `ducksy.storage` to remember things.
- **Features can't:** read or write files, run programs, call other websites, touch the bot's
  token, kick, ban, or make the bot leave a server. Duck$y also can't ping @everyone or
  roles, whatever a feature says.
- Want a feature that calls some other website (GIFs, weather, sports scores)? Ask Nick: he can
  add a safe helper for it to the core, and then anyone can use it.

## Good first ideas

Magic 8-ball, /roast, trivia with buttons, a daily "duck fact", a leaderboard for /quack,
a countdown to the next big game, "who's the worst gambler" from the DucksBucks bets.
