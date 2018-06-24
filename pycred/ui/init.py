import logging
import os
import sys

import click

from . import DEFAULT_CONTEXT_SETTINGS
from ..pycred import PyCred

logger = logging.getLogger('init')
logger.addHandler(logging.NullHandler())

_pycred = PyCred()
_config = _pycred.get_config()
_serializers = _config.serializers
_encryptions = _config.encryptions
_storages = _config.storages


@click.command('init', context_settings=DEFAULT_CONTEXT_SETTINGS)
@click.option(
    '--serializer',
    type=click.Choice(_serializers.get_backend_names()),
    default=_serializers.default,
    help='Serializer to use.',
    show_default=True)
@click.option(
    '--encryption',
    type=click.Choice(_encryptions.get_backend_names()),
    default=_encryptions.default,
    help='Encryption to use.',
    show_default=True)
@click.option(
    '--storage',
    type=click.Choice(_storages.get_backend_names()),
    default=_storages.default,
    help='Storage to use.',
    show_default=True)
@click.argument('name', nargs=1, required=True)
@click.pass_context
def init(ctx, serializer, encryption, storage, name):
    """Initialize new store with name NAME."""
    logger.debug(
        "name={name}, serializer={se}, encryption={en}, storage={st}".format(
            name=name, se=serializer, en=encryption, st=storage))
    try:
        logger.debug("store_path={sp}".format(sp=_config.get_store_path()))
        os.makedirs(_config.get_store_path(), mode=0o700, exist_ok=True)
        _pycred.init_store(name, serializer, encryption, storage)
    except Exception as e:
        logger.debug(e, exc_info=True)
        print('Error: {msg}'.format(msg=str(e)), file=sys.stderr)
        sys.exit(1)
