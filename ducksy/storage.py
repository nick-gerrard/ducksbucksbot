"""Tiny per-feature storage so features can remember things (scores, counters, ...).

    from ducksy.storage import Store

    quacks = Store("quacks")
    data = quacks.load()          # a dict; empty the first time
    data["total"] = data.get("total", 0) + 1
    quacks.save(data)

Each feature gets its own JSON file. Keep it small: this is for fun stats, not big data.
"""

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any

_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,40}$")
MAX_BYTES = 256 * 1024


def data_dir() -> Path:
    # systemd sets STATE_DIRECTORY for the deployed bot; locally it's ./data
    return Path(os.environ.get("STATE_DIRECTORY") or os.environ.get("DUCKSY_DATA_DIR") or "data")


class Store:
    def __init__(self, name: str):
        if not _NAME_RE.match(name):
            raise ValueError(f"store name must be lowercase letters/numbers/-/_, got {name!r}")
        self.name = name

    @property
    def path(self) -> Path:
        return data_dir() / f"{self.name}.json"

    def load(self) -> dict[str, Any]:
        try:
            return json.loads(self.path.read_text())
        except FileNotFoundError:
            return {}

    def save(self, data: dict[str, Any]) -> None:
        text = json.dumps(data, indent=2, sort_keys=True)
        if len(text.encode()) > MAX_BYTES:
            raise ValueError(f"store {self.name!r} is over {MAX_BYTES // 1024} KB; keep less data")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, prefix=f".{self.name}.")
        with os.fdopen(fd, "w") as f:
            f.write(text)
        os.replace(tmp, self.path)
