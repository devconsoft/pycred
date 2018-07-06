import logging

import click
import coloredlogs

import pycred

from . import DEFAULT_CONTEXT_SETTINGS
from .get import get_credentials
from .help import help
from .info import info
from .init import init
from .list import liststores
from .rm import rm
from .set import set_credentials
from .unset import unset_credentials


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
    """Interact with pycred, its stores and configuration."""
    verbosity_levels = (logging.WARNING, logging.INFO, logging.DEBUG)
    level = verbosity_levels[verbose]
    fmt = '%(asctime)s %(name)s %(levelname)s %(message)s'
    coloredlogs.install(level=level, fmt=fmt)


main.add_command(get_credentials)
main.add_command(help)
main.add_command(info)
main.add_command(init)
main.add_command(liststores)
main.add_command(rm)
main.add_command(set_credentials)
main.add_command(unset_credentials)

if __name__ == '__main__':
    main()
