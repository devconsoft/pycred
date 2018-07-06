import tempfile
from unittest.mock import patch


def test_set_long_opt_help(pycred):
    pycred('set --help')


def test_set_short_opt_help(pycred):
    pycred('set -h')


def test_set_none_existing_store_gives_exit_code_2(pycred):
    with tempfile.TemporaryDirectory(prefix='pycred-') as d:
        with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
            pycred('set non-existing-store user', expected_exit_code=2)
