def test_help_defaults_to_html(pycred):
    result = pycred('help --print-path')
    assert 'index.html' in result.stdout, result.stdout


def test_help_html(pycred):
    result = pycred('help --html --print-path')
    assert 'index.html' in result.stdout, result.stdout


def test_help_pdf(pycred):
    result = pycred('help --pdf --print-path')
    assert 'user_guide.pdf' in result.stdout, result.stdout


def test_help_long_opt_help(pycred):
    pycred('help --help')


def test_help_short_opt_help(pycred):
    pycred('help -h')


def test_both_html_and_pdf_gives_error(pycred):
    result = pycred('help --html --pdf', expected_exit_code=1)
    assert 'Error: ' in result.stderr, result.stderr
