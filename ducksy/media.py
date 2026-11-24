"""Reviewed door for features to attach media files (memes, images, etc.).

Features can't touch the filesystem directly (`open`, `pathlib`, `discord.File` are blocked by
the safety check), so this module is the one reviewed place that reads images from disk.

Nick drops images into `<state dir>/media/<name>/` on the server (for example,
`/var/lib/ducksy/media/call` for `/call`).
"""

import random
import re
from pathlib import Path

import discord

from ducksy.storage import data_dir

_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,40}$")
IMAGE_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".gif", ".webp"})


def media_dir(name: str) -> Path:
    """Return `<state dir>/media/<name>`, creating it if needed."""
    if not _NAME_RE.match(name):
        raise ValueError(f"media name must be lowercase letters/numbers/-/_, got {name!r}")
    path = data_dir() / "media" / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def random_image(name: str) -> discord.File | None:
    """Pick a random image from `media_dir(name)`, or return None if there are none."""
    directory = media_dir(name)
    candidates = [
        p
        for p in directory.iterdir()
        if p.is_file() and not p.name.startswith(".") and p.suffix.lower() in IMAGE_SUFFIXES
    ]
    if not candidates:
        return None
    chosen = random.choice(candidates)
    return discord.File(chosen, filename=chosen.name)
