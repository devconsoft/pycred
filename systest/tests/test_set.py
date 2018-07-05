def test_set_long_opt_help(pycred):
    pycred('set --help')


def test_set_short_opt_help(pycred):
    pycred('set -h')


def test_set_none_existing_store_gives_exit_code_2(pycred):
    pycred('set non-existing-store user', expected_exit_code=2)
