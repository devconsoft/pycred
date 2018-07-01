from unittest.mock import patch

from systest import get_stores_dir


def test_list_long_opt_help(pycred):
    pycred('list --help')


def test_list_short_opt_help(pycred):
    pycred('list -h')


def test_list(pycred):
    with patch.dict('os.environ', {'PYCRED_STORE_PATH': get_stores_dir()}):
        result = pycred('list')
    expected = """\
s1
s2
"""
    assert expected == result.stdout, result.stdout
