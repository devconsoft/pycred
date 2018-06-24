import logging
import sys

import click

from . import DEFAULT_CONTEXT_SETTINGS
from ..pycred import PyCred

logger = logging.getLogger('list')
logger.addHandler(logging.NullHandler())


@click.command('list', context_settings=DEFAULT_CONTEXT_SETTINGS)
@click.pass_context
def liststores(ctx):
    """List all stores by name."""
    try:
        for name in PyCred().get_store_names():
            print(name)
    except Exception as e:
        logger.debug(e, exc_info=True)
        print('Error: {msg}'.format(msg=str(e)), file=sys.stderr)
        sys.exit(1)
