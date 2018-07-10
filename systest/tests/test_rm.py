def test_rm_long_opt_help(pycred):
    pycred('rm --help')


def test_rm_short_opt_help(pycred):
    pycred('rm -h')


def test_rm_none_existing_store_gives_exit_code_2(pycred, workspace):
    with workspace():
        pycred('rm non-existing-store user', expected_exit_code=2)
