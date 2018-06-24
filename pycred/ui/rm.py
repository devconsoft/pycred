import logging
import sys

import click

from . import DEFAULT_CONTEXT_SETTINGS
from ..pycred import PyCred

logger = logging.getLogger('rm')
logger.addHandler(logging.NullHandler())

_pycred = PyCred()
_stores = _pycred.get_store_names()


@click.command('rm', context_settings=DEFAULT_CONTEXT_SETTINGS)
@click.argument('names', nargs=-1, required=True, type=click.Choice(_stores))
@click.pass_context
def rm(ctx, names):
    """
    Delete selected store(s).

    Mulitple names can be supplied.
    """
    logger.debug("names=[{names}]".format(names=', '.join(names)))
    try:
        for name in names:
            _pycred.delete_store(name)
    except Exception as e:
        logger.debug(e, exc_info=True)
        print('Error: {msg}'.format(msg=str(e)), file=sys.stderr)
        sys.exit(1)
