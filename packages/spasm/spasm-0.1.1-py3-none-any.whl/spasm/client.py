"""Define our IRC client and relevant methods."""

from pydle import Client

from spasm import config


class SpasmClient(Client):
    """A simple IRC client that outputs messages to stdout."""

    async def on_connect(self) -> None:
        """Join the relevant channel for the provided user."""
        for channel in config.channels:
            await self.join(f"#{channel}")

    async def on_message(self, target: str, source: str, message: str) -> None:
        """Log all messages sent to relevant channels to stdout."""
        print(f"{target} {source:>25}  {message}", flush=True)
