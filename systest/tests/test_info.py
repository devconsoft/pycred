import tempfile
import uuid
from unittest.mock import patch


def test_info_long_opt_help(pycred):
    pycred('info --help')


def test_info_short_opt_help(pycred):
    pycred('info -h')


def test_info_none_existing_store_gives_exit_code_2(pycred):
    with tempfile.TemporaryDirectory(prefix='pycred-') as d:
        with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
            pycred('info non-existing-store user', expected_exit_code=2)


def test_info_std_format(pycred):
    with tempfile.TemporaryDirectory(prefix='pycred-') as d:
        with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
            pycred('init mystore --storage memory --encryption clear --serializer json')
            result = pycred('info mystore -f std')
            expected = """\
mystore
encryption: clear
serializer: json
storage: memory
"""
            assert result.stdout == expected


def test_info_raw_format(pycred):
    with tempfile.TemporaryDirectory(prefix='pycred-') as d:
        with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
            pycred('init mystore --storage memory --encryption clear --serializer json')
            result = pycred('info mystore --format raw')
            output = result.stdout
            assert '!StoreConfig' in output
            assert 'memory' in output
            assert 'clear' in output
            assert 'json' in output


def test_info_none_format(pycred):
    with tempfile.TemporaryDirectory(prefix='pycred-') as d:
        with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
            pycred('init mystore --storage memory --encryption clear --serializer json')
            result = pycred('info mystore --format none')
            assert result.stdout == 'mystore\n'


def test_info_users(pycred):
    with tempfile.TemporaryDirectory(prefix='pycred-') as d:
        with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
            store_name = uuid.uuid4()
            pycred(
                'init {name} --storage file --encryption clear --serializer json'.format(
                    name=store_name))
            pycred('set --user USER1 --password P {name} U'.format(name=store_name))
            pycred('set --user USER2 --password P {name} U'.format(name=store_name))
            result = pycred('info {name} --format none --users'.format(name=store_name))
            assert 'users: USER1, USER2\n' in result.stdout
