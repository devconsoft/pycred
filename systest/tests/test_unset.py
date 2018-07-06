import tempfile
from unittest.mock import patch


def test_unset_long_opt_help(pycred):
    pycred('unset --help')


def test_unset_short_opt_help(pycred):
    pycred('unset -h')


def test_unset_none_existing_store_gives_exit_code_2(pycred):
    with tempfile.TemporaryDirectory(prefix='pycred-') as d:
        with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
            pycred('unset non-existing-store user', expected_exit_code=2)
