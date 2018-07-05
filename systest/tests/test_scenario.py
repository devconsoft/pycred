import tempfile
from unittest.mock import patch


def test_scenario_init_list_set_get_unset_rm_for_json_clear_file_store(pycred):
    with tempfile.TemporaryDirectory(prefix='pycred-') as d:
        with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
            pycred('init mystore')
            assert pycred('list').stdout == 'mystore\n'
            pycred('set mystore -u USER --password P U')
            assert pycred('get mystore -u USER --password').stdout == 'P\n'
            assert pycred('get mystore -u USER --username').stdout == 'U\n'
            assert pycred('get mystore -u USER --password --username').stdout == 'U\nP\n'
            assert "Unsetting credentials for user 'USER' in store 'mystore'" in pycred(
                '-v unset mystore -u USER').stderr
            assert "Deleting store 'mystore'" in pycred('-v rm mystore').stderr
