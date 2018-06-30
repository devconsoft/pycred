import unittest
from unittest.mock import mock_open, patch

from .. import GetDataFailed, InvalidUser, SetDataFailed
from ..file import FileStorage


class TestFileStorage(unittest.TestCase):

    data = 'data'

    def get_filestorage(self):
        s = FileStorage('data_dir')
        return s

    def test_get_data(self):
        with patch('builtins.open', new_callable=mock_open, read_data=self.data) as m:
            s = self.get_filestorage()
            result = s.get_data('user')
            m.assert_called_with('data_dir/user.dat', 'r')
            self.assertEqual(self.data, result)

    def test_set_data(self):
        with patch('builtins.open', new_callable=mock_open) as m, patch('os.makedirs'):
            s = self.get_filestorage()
            s.set_data('user', self.data)
            m.assert_called_with('data_dir/user.dat', 'w')
            m().write.assert_called_with(self.data)

    def test_raises_invaliduser_if_the_user_is_not_found(self):
        s = FileStorage('/invalid/random/path')
        with self.assertRaises(InvalidUser):
            s.get_data('user')

    def test_raises_get_data_failed_for_permission_errors(self):
        with patch('builtins.open', side_effect=PermissionError()):
            s = FileStorage('data_dir')
            with self.assertRaises(GetDataFailed):
                s.get_data('user')

    def test_raises_set_data_failed(self):
        s = FileStorage('/invalid/random/path')
        with self.assertRaises(SetDataFailed):
            s.set_data('user', self.data)

    def test_delete(self):
        s = self.get_filestorage()
        with patch('shutil.rmtree') as m, patch('os.path.isdir', return_value=True):
            s.delete()
        m.assert_called_with('data_dir')
