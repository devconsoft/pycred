
def test_help_defaults_to_html(pycred):
    result = pycred('help --print-path')
    assert 'index.html' in result.stdout, result.stderr


def test_help_html(pycred):
    result = pycred('help --html --print-path')
    assert 'index.html' in result.stdout, result.stderr


def test_help_pdf(pycred):
    result = pycred('help --pdf --print-path')
    assert 'user_guide.pdf' in result.stdout, result.stderr
