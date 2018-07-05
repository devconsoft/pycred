import logging
import sys

import click

from . import DEFAULT_CONTEXT_SETTINGS
from ..pycred import PyCred

logger = logging.getLogger('set')
logger.addHandler(logging.NullHandler())

_pycred = PyCred()
_stores = _pycred.get_store_names()


@click.command('set', context_settings=DEFAULT_CONTEXT_SETTINGS)
@click.option('--user', '-u', help='User', default=_pycred.get_default_user(), show_default=True)
@click.password_option()
@click.argument('store', nargs=1, required=True, type=click.Choice(_stores))
@click.argument('username', nargs=1, required=True)
@click.pass_context
def set_credentials(ctx, user, store, username, password):
    """
    Set credentials (username and password) for the USER in STORE.

    Alternative user can be specified with --u/-u. Defaults to the current user.

    It is recommended not to use the password option and instead enter it when
    prompted for it.
    """
    try:
        logger.debug(
            "store={store}, user={user}, username={username}".format(
                store=store, user=user, username=username))
        _pycred.set_credentials(store, username, password, user)
    except Exception as e:
        logger.debug(e, exc_info=True)
        print('Error: {msg}'.format(msg=str(e)), file=sys.stderr)
        sys.exit(1)
