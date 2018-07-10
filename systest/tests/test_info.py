import uuid


def test_info_long_opt_help(pycred):
    pycred('info --help')


def test_info_short_opt_help(pycred):
    pycred('info -h')


def test_info_none_existing_store_gives_exit_code_2(pycred, workspace):
    with workspace():
        pycred('info non-existing-store user', expected_exit_code=2)


def test_info_std_format(pycred, workspace):
    with workspace() as ws:
        pycred('init mystore --storage memory --encryption clear --serializer json')
        result = pycred('info mystore -f std')
        expected = """\
name: mystore
config-file: {d}/mystore.yaml
encryption: clear
serializer: json
storage: memory
""".format(d=ws.path)
        assert result.stdout == expected, result.stdout


def test_info_raw_format(pycred, workspace):
    with workspace():
        pycred('init mystore --storage memory --encryption clear --serializer json')
        result = pycred('info mystore --format raw')
        output = result.stdout
        assert '!StoreConfig' in output
        assert 'memory' in output
        assert 'clear' in output
        assert 'json' in output


def test_info_none_format(pycred, workspace):
    with workspace() as ws:
        pycred('init mystore --storage memory --encryption clear --serializer json')
        result = pycred('info mystore --format none')
        assert result.stdout == 'name: mystore\nconfig-file: {d}/mystore.yaml\n'.format(
            d=ws.path), result.stdout


def test_info_users(pycred, workspace):
    with workspace():
        store_name = uuid.uuid4()
        pycred(
            'init {name} --storage file --encryption clear --serializer json'.format(
                name=store_name))
        pycred('set --user USER1 --password P {name} U'.format(name=store_name))
        pycred('set --user USER2 --password P {name} U'.format(name=store_name))
        result = pycred('info {name} --format none --users'.format(name=store_name))
        assert 'users: USER1, USER2\n' in result.stdout
