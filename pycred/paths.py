import inspect
from functools import lru_cache
from os.path import dirname, join

import pycred


@lru_cache(maxsize=1)
def get_pycred_dir():
    return dirname(inspect.getfile(pycred))


@lru_cache(maxsize=1)
def get_doc_dir():
    path = get_pycred_dir()
    if path.startswith('/opt/venvs/pycred/'):
        return '/opt/venvs/pycred/doc'
    else:
        return join(dirname(path), 'build', 'doc')


@lru_cache(maxsize=1)
def get_config_dir():
    pass
