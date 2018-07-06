import tempfile
from unittest.mock import patch


def test_init_long_opt_help(pycred):
    pycred('init --help')


def test_init_short_opt_help(pycred):
    pycred('init -h')


def test_init_existing_store_gives_exit_code_2(pycred):
    with tempfile.TemporaryDirectory(prefix='pycred-') as d:
        with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
            pycred('init mystore --storage memory')
            result = pycred('init mystore', expected_exit_code=2)
            assert "Store mystore already exists" in result.stderr, result.stderr
