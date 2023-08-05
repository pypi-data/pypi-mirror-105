"""Define our IRC client and relevant methods."""

from datetime import datetime

from colorama import Back, Fore, Style
from pydle import Client

from spasm import config


class SpasmClient(Client):
    """A simple IRC client that outputs messages to stdout."""

    async def on_connect(self) -> None:
        """Join the relevant channel for the provided user."""
        for channel in config.channels:
            await self.join(f"#{channel}")

    async def on_message(self, _: str, source: str, message: str) -> None:
        """Log all messages sent to relevant channels to stdout."""
        timestamp = datetime.now().time().strftime("%H:%S")
        print(
            (
                f"{Fore.LIGHTWHITE_EX}{timestamp}  "
                f"{Fore.BLUE}{source:>23}{Fore.WHITE}:  "
                f"{Fore.WHITE}{message}{Style.RESET_ALL}"
            ),
            flush=True,
        )
