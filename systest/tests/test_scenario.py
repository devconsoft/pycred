def test_scenario_init_list_set_get_unset_rm_for_json_clear_file_store(pycred, workspace):
    with workspace():
        pycred('init mystore --encryption clear --storage file --serializer json')
        assert pycred('list').stdout == 'mystore\n'
        pycred('set mystore -u USER --password P U')
        assert pycred('get mystore -u USER --password').stdout == 'P\n'
        assert pycred('get mystore -u USER --username').stdout == 'U\n'
        assert pycred('get mystore -u USER --password --username').stdout == 'U\nP\n'
        assert "Unsetting credentials for user 'USER' in store 'mystore'" in pycred(
            '-v unset mystore -u USER').stderr
        assert "Deleting store 'mystore'" in pycred('-v rm mystore').stderr


def test_scenario_init_list_set_get_unset_rm_for_json_aes_file_store(pycred, workspace):
    with workspace():
        pycred('init mystore --encryption aes --storage file --serializer json')
        assert pycred('list').stdout == 'mystore\n'
        pycred('set mystore -u USER --password P U')
        assert pycred('get mystore -u USER --password').stdout == 'P\n'
        assert pycred('get mystore -u USER --username').stdout == 'U\n'
        assert pycred('get mystore -u USER --password --username').stdout == 'U\nP\n'
        assert "Unsetting credentials for user 'USER' in store 'mystore'" in pycred(
            '-v unset mystore -u USER').stderr
        assert "Deleting store 'mystore'" in pycred('-v rm mystore').stderr
