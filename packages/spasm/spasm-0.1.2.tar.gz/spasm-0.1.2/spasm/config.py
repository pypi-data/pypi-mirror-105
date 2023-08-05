"""Relevant constants or config options used throughout the project."""

import os
from typing import Final


channels: list[str] = []

USERNAME: Final[str] = os.getenv("TWITCH_USERNAME") or ""
PASSWORD: Final[str] = os.getenv("TWITCH_OAUTH_PASSWORD") or ""
