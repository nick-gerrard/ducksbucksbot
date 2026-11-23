# Duck$y 🦆

The official mascot of [DucksBucks](https://ducksbucks.nickgerrard.dev): a Discord bot that posts
today's games and open bets, and does whatever other fun things the crew adds.

## 👉 Want to add something? Read the [guide](GUIDE.md)

You don't need to be a programmer or have a computer. Paste one prompt into the Claude,
ChatGPT or Gemini app on your phone, and the [guide](GUIDE.md) takes you from idea to live in
Discord. Looking for something to build? Check the
[idea board](https://github.com/nick-gerrard/ducksbucksbot/issues?q=is%3Aopen+label%3Aidea).

## How it works

```
ducksy/
  bot.py            the core: loads every feature, keeps mentions safe, handles errors (Nick's)
  ducksbucks.py     reads games and bets from the DucksBucks site (Nick's)
  storage.py        lets features remember things between restarts (Nick's)
  settings.py       channel ID and timezone (Nick's)
  features/         ONE FILE PER FEATURE: this is where new stuff goes
    basics.py       /ping, /intro, /gamblers
    daily_posts.py  /today, /bets, and the daily 10am and 6pm Eastern posts
    quack.py        /quack, /coinflip (a small example to copy)
scripts/safety_check.py   the safety gate every PR goes through
tests/                    checks that run on every PR
```

## Running it locally

```bash
uv sync
uv run pytest            # tests, no Discord needed
cp .env.example .env     # then fill in a bot token for a *test* bot
uv run python -m ducksy
```

## Deploying

Pushes to `main` deploy to Nick's server with [roost](https://github.com/nick-gerrard/roost)
once CI passes (`deploy.toml`). The bot runs as a background worker in a systemd sandbox: it
can't see the rest of the server, and only `data/`-style state survives restarts.
Secrets (`DISCORD_TOKEN`, `CHANNEL_ID`) live in the server's env file, never in git.
