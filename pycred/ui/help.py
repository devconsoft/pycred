import click

from . import DEFAULT_CONTEXT_SETTINGS
from ..help import openhelp


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
    try:
        openhelp(html, pdf, print_path)
    except Exception as e:
        print('Error: {msg}'.format(msg=str(e)))
        exit(1)
