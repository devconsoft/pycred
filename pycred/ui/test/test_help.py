import unittest
from unittest.mock import patch

from click.testing import CliRunner

from ..help import help


class TestHelp(unittest.TestCase):

    @patch('pycred.ui.help.openhelp')
    def test_commandline_parsing_all_opts(self, mock_openhelp):
        runner = CliRunner()
        runner.invoke(help, ['--html', '--pdf', '--print-path'])
        mock_openhelp.assert_called_with(True, True, True)
