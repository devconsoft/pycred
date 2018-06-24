import logging
import sys

import click

from . import DEFAULT_CONTEXT_SETTINGS
from ..help import openhelp

logger = logging.getLogger('help')
logger.addHandler(logging.NullHandler())


@click.command('help', context_settings=DEFAULT_CONTEXT_SETTINGS)
@click.option('--html', is_flag=True, default=False, help='Open HTML documentation.')
@click.option('--pdf', is_flag=True, default=False, help='Open PDF documentation.')
@click.option('--print-path', is_flag=True, default=False, help='Print path instead of opening it.')
@click.pass_context
def help(ctx, html, pdf, print_path):
    """
    Open PyCred user-guide as HTML or PDF.

    Only one format can be specified, defaults to HTML.
    """
    logger.debug(
        "html={html}, pdf={pdf}, print-path=${print_path}".format(
            html=html, pdf=pdf, print_path=print_path))
    try:
        openhelp(html, pdf, print_path)
    except Exception as e:
        logger.debug(e, exc_info=True)
        print('Error: {msg}'.format(msg=str(e)), file=sys.stderr)
        sys.exit(1)
