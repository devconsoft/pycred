import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

from ..help import FailedToOpenHelp, MultipleFormats, openhelp


class TestOpenHelp(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_openhelp_print_default(self, mock_stdout):
        openhelp(False, False, True)
        self.assertIn('index.html', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_openhelp_print_html(self, mock_stdout):
        openhelp(True, False, True)
        self.assertIn('index.html', mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_openhelp_print_pdf(self, mock_stdout):
        openhelp(False, True, True)
        self.assertIn('user_guide.pdf', mock_stdout.getvalue())

    def test_openhelp_raises_exception_if_multiple_formats(self):
        with self.assertRaises(MultipleFormats):
            openhelp(True, True, True)

    @patch('subprocess.call', new_callable=MagicMock())
    def test_openhelp_open_with_application(self, mock_call):
        openhelp(False, False, False)
        ((_, filepath), ), _ = mock_call.call_args
        self.assertIn('index.html', filepath)

    @patch('subprocess.call', side_effect=Exception('Error'))
    def test_openhelp_raises_exception_if_fails_to_open(self, mock_call):
        with self.assertRaises(FailedToOpenHelp):
            openhelp(False, False, False)
