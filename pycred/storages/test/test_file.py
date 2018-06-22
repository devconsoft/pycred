import unittest
from io import StringIO
from unittest.mock import mock_open, patch

from .. import GetDataFailed, SetDataFailed
from ..file import FileStorage


class TestFileStorage(unittest.TestCase):

    data = 'data'

    def test_get_data(self):
        with patch('builtins.open', new_callable=mock_open, read_data=self.data):
            s = FileStorage('data_dir')
            result = s.get_data('user')
            self.assertEqual(self.data, result)

    def test_set_data(self):
        with patch('builtins.open', new_callable=mock_open) as m:
            s = FileStorage('data_dir')
            s.set_data('user', self.data)
            m.assert_called_with('data_dir/user.dat', 'w')
            m().write.assert_called_with(self.data)


    def test_raises_get_data_failed(self):
        s = FileStorage('/invalid/random/path')
        with self.assertRaises(GetDataFailed):
            s.get_data('user')

    def test_raises_set_data_failed(self):
        s = FileStorage('/invalid/random/path')
        with self.assertRaises(SetDataFailed):
            s.set_data('user', self.data)
