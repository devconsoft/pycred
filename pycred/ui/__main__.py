import logging

import click
import coloredlogs

import pycred

from . import DEFAULT_CONTEXT_SETTINGS
from .help import help


@click.group(context_settings=DEFAULT_CONTEXT_SETTINGS)
@click.option(
    "-v",
    "--verbose",
    count=True,
    type=click.IntRange(0, 2, clamp=True),
    help="Increase output verbosity.")
@click.version_option(pycred.__version__)
@click.pass_context
def main(ctx, verbose):
    """Interact with pycred credentials storage."""
    verbosity_levels = (logging.WARNING, logging.INFO, logging.DEBUG)
    coloredlogs.install(level=verbosity_levels[verbose])


main.add_command(help)

if __name__ == '__main__':
    main()
