import tempfile
from unittest.mock import patch


def test_rm_long_opt_help(pycred):
    pycred('rm --help')


def test_rm_short_opt_help(pycred):
    pycred('rm -h')


def test_rm_none_existing_store_gives_exit_code_2(pycred):
    with tempfile.TemporaryDirectory(prefix='pycred-') as d:
        with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
            pycred('rm non-existing-store user', expected_exit_code=2)
