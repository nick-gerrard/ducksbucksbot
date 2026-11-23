"""Read-only access to the DucksBucks site (https://ducksbucks.nickgerrard.dev)."""

from typing import Any

import aiohttp

BASE_URL = "https://ducksbucks.nickgerrard.dev/api"
_TIMEOUT = aiohttp.ClientTimeout(total=10)


async def _get(path: str) -> dict[str, Any]:
    async with aiohttp.ClientSession(timeout=_TIMEOUT) as session:
        async with session.get(f"{BASE_URL}/{path}") as resp:
            resp.raise_for_status()
            return await resp.json()


async def todays_games() -> list[dict[str, Any]]:
    """Each game has `home`, `away` and `start_time`."""
    return (await _get("todays-games"))["games"]


async def pending_bets() -> list[dict[str, Any]]:
    """Each bet has `challenger`, `challengee`, `amount`, `challenger_pick`, `challengee_pick`."""
    return (await _get("pending-bets"))["bets"]


def format_games(games: list[dict[str, Any]]) -> str:
    if not games:
        return (
            "Sorry, no games scheduled today. You'll hafta gamble on something else.\n"
            "Might I recommend the upcoming fight between Hammy and Churchy???"
        )
    return "\n".join(f"{g['home']} VS {g['away']} @ {g['start_time']}" for g in games)


def format_bets(bets: list[dict[str, Any]]) -> str:
    if not bets:
        return "No unresolved bets today."
    return "\n".join(
        f"{b['challenger']} bet {b['challengee']} {b['amount']} DucksBucks "
        f"on {b['challenger_pick']} to beat {b['challengee_pick']}"
        for b in bets
    )
