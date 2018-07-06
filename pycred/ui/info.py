import logging
import sys

import click

from . import DEFAULT_CONTEXT_SETTINGS
from ..config import ConfigurationManager
from ..pycred import PyCred

logger = logging.getLogger('info')
logger.addHandler(logging.NullHandler())

_pycred = PyCred()
_stores = _pycred.get_store_names()


@click.command('info', context_settings=DEFAULT_CONTEXT_SETTINGS)
@click.option(
    '--format',
    '-f',
    default='std',
    show_default=True,
    type=click.Choice(['std', 'raw', 'none']),
    help='The output format of the store info.')
@click.option(
    '--users', '-u', default=False, is_flag=True, show_default=True, help='Show the stores users.')
@click.argument('names', nargs=-1, required=True, type=click.Choice(_stores))
@click.pass_context
def info(ctx, names, format, users):
    """
    Show info about selected store(s).

    Multiple names can be supplied.

    """
    try:
        logger.debug(
            "names=[{names}], format={format}, users={users}".format(
                names=', '.join(names), format=format, users=users))
        config = ConfigurationManager()
        for name in names:
            print(name)
            if format == 'std':
                store_cfg = config.get_store_config(name)
                print('encryption: {encryption}'.format(encryption=store_cfg.encryption.name))
                print('serializer: {serializer}'.format(serializer=store_cfg.serializer.name))
                print('storage: {storage}'.format(storage=store_cfg.storage.name))
            elif format == 'raw':
                print(config.get_raw_config(name))
            elif format == 'none':
                pass
            if users:
                store_users = _pycred.get_store(name).get_users()
                print('users: {users}'.format(users=', '.join(store_users)))
    except Exception as e:
        logger.debug(e, exc_info=True)
        print('Error: {msg}'.format(msg=str(e)), file=sys.stderr)
        sys.exit(1)
