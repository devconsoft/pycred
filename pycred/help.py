import os
import subprocess

from .paths import get_doc_dir


class MultipleFormats(Exception):
    pass


class FailedToOpenHelp(Exception):
    pass


def openhelp(html, pdf, print_path):
    root = get_doc_dir()
    path = None

    if pdf and html:
        raise MultipleFormats(
            'Error: Multiple documentation formats specified. Specify either --html or --pdf')
    elif pdf:
        path = os.path.join(root, 'user_guide/pdf/user_guide.pdf')
    else:
        path = os.path.join(root, 'user_guide/html/index.html')

    if print_path:
        print(path)
    else:
        _open_with_application(path)


def _open_with_application(filepath):
    try:
        subprocess.call(('xdg-open', filepath))
    except Exception as e:
        raise FailedToOpenHelp(
            "Failed when trying to use 'xdg-open' to open '{path}': {msg}".format(
                path=filepath, msg=str(e)))
