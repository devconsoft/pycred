def test_unset_long_opt_help(pycred):
    pycred('unset --help')


def test_unset_short_opt_help(pycred):
    pycred('unset -h')


def test_unset_none_existing_store_gives_exit_code_2(pycred):
    pycred('unset non-existing-store user', expected_exit_code=2)
