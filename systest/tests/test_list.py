from unittest.mock import patch
import os
import tempfile


def test_list_long_opt_help(pycred):
    pycred('list --help')


def test_list_short_opt_help(pycred):
    pycred('list -h')


def test_list(pycred):
    with tempfile.TemporaryDirectory(prefix='pycred-') as d:
        with open(os.path.join(d, "s1.yaml"), 'w+'):
            pass
        with open(os.path.join(d, "s2.yaml"), 'w+'):
            pass
        with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
            result = pycred('list')
    expected = """\
s1
s2
"""
    assert expected == result.stdout, result.stdout
