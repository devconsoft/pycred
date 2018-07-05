import logging
import sys

import click

from . import DEFAULT_CONTEXT_SETTINGS
from ..pycred import PyCred

logger = logging.getLogger('unset')
logger.addHandler(logging.NullHandler())

_pycred = PyCred()
_stores = _pycred.get_store_names()


@click.command('unset', context_settings=DEFAULT_CONTEXT_SETTINGS)
@click.option('--user', '-u', help='User', default=_pycred.get_default_user(), show_default=True)
@click.argument('store', nargs=1, required=True, type=click.Choice(_stores))
@click.pass_context
def unset_credentials(ctx, user, store):
    """
    Unset credentials for the USER in STORE.

    Alternative user can be specified with --user/-u. Defaults to the current user.
    """
    try:
        logger.debug("store={store}, user={user}".format(store=store, user=user))
        _pycred.unset_credentials(store, user)
    except Exception as e:
        logger.debug(e, exc_info=True)
        print('Error: {msg}'.format(msg=str(e)), file=sys.stderr)
        sys.exit(1)
