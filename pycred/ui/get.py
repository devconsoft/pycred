import logging
import sys

import click

from . import DEFAULT_CONTEXT_SETTINGS
from ..pycred import PyCred

logger = logging.getLogger('get')
logger.addHandler(logging.NullHandler())

_pycred = PyCred()
_stores = _pycred.get_store_names()


@click.command('get', context_settings=DEFAULT_CONTEXT_SETTINGS)
@click.option('--user', '-u', help='User', default=_pycred.get_default_user(), show_default=True)
@click.argument('store', nargs=1, required=True, type=click.Choice(_stores))
@click.option(
    '--username', '-n', help='Show username', default=False, show_default=True, is_flag=True)
@click.option(
    '--password', '-p', help='Show password', default=False, show_default=True, is_flag=True)
@click.pass_context
def get_credentials(ctx, user, store, username, password):
    """
    Get credentials (username and password printed to stdout) for the USER in STORE.

    Alternative user can be specified with --u/-u. Defaults to the current user.

    --username and --password can be used to set what should be shown.
    If neither is specified, the command only returns without printing anything, but
    with exit code zero to indicate that credentials exist for the specified user.

    If the user doesn't exist, the program exits with exit code 3.
    """
    try:
        logger.debug(
            "store={store}, user={user}, username={username}".format(
                store=store, user=user, username=username))
        credentials = _pycred.get_credentials(store, user)
        if credentials is None:
            print(
                "User '{user}' does not exist in store '{store}'.".format(user=user, store=store),
                file=sys.stderr)
            sys.exit(3)
        if username:
            print(credentials.username)
        if password:
            print(credentials.password)
    except Exception as e:
        logger.debug(e, exc_info=True)
        print('Error: {msg}'.format(msg=str(e)), file=sys.stderr)
        sys.exit(1)
