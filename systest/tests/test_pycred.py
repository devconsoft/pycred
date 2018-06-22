
def test_version(pycred):
    pycred('--version')


def test_help_long_form(pycred):
    pycred('--help')


def test_help_short_form(pycred):
    pycred('-h')
