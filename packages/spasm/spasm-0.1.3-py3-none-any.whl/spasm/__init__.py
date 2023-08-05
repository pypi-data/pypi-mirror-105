"""Spasm - A simple twitch.tv chat viewer.

Usage:
  spasm stream <name>...
  spasm (-h | --help)
  spasm --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import contextlib, os
from docopt import docopt
from pkg_resources import get_distribution

from spasm import config
from spasm.client import SpasmClient


__version__ = get_distribution("spasm").version


def main() -> None:
    """Entrypoint for the command-line script, called by poetry."""
    arguments = docopt(__doc__, version=f"Spasm {__version__}")

    for channel in arguments.get("<name>", ()):
        config.channels.append(channel.lower())

    client = SpasmClient(config.USERNAME, realname=config.USERNAME)
    with contextlib.redirect_stderr(open(os.devnull)):
        client.run("irc.twitch.tv", tls=False, password=config.PASSWORD)
