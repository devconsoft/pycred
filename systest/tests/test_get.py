def test_get_long_opt_help(pycred):
    pycred('get --help')


def test_get_short_opt_help(pycred):
    pycred('get -h')


def test_get_none_existing_store_gives_exit_code_2(pycred, workspace):
    with workspace():
        pycred('get non-existing-store user', expected_exit_code=2)


def test_get_none_existing_user_gives_exit_code_3(pycred, workspace):
    with workspace():
        pycred('init mystore --storage memory')
        try:
            result = pycred('get mystore -u USER', expected_exit_code=3)
            assert "Error: User 'USER' does not exist in store 'mystore'." in result.stderr
        finally:
            pycred('rm mystore')
