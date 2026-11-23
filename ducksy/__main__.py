"""Start Duck$y: `uv run python -m ducksy`."""

import logging
import os

from dotenv import load_dotenv

from ducksy.bot import Ducksy


def main() -> None:
    load_dotenv()
    # Take the token out of the environment so nothing else in the process can read it there.
    token = os.environ.pop("DISCORD_TOKEN", None)
    if not token:
        raise SystemExit("DISCORD_TOKEN is not set (put it in .env for local runs)")
    Ducksy().run(token, log_level=logging.INFO, root_logger=True)


if __name__ == "__main__":
    main()
