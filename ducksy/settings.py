"""Non-secret settings that features may read."""

import os
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

# The channel Duck$y posts its daily updates in. None when unset (e.g. in tests).
_channel = os.environ.get("CHANNEL_ID", "").strip()
CHANNEL_ID: int | None = int(_channel) if _channel else None

# The DucksBucks crew lives on Eastern time; schedule things in this zone.
TIMEZONE = ZoneInfo("America/New_York")
