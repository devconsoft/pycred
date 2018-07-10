import os
import tempfile
import unittest
from unittest.mock import mock_open, patch

from .. import GetDataFailed, InvalidUser, SetDataFailed, UnsetDataFailed
from ..file import FileStorage


class TestFileStorage(unittest.TestCase):

    data = 'data'

    def get_filestorage(self):
        fs = FileStorage('data_dir')
        return fs

    @patch('pycred.storages.file.create_secure_file')
    @patch('pycred.storages.file.check_file_security')
    def test_get_data(self, create_mock, check_mock):
        with patch('builtins.open', new_callable=mock_open, read_data=self.data) as m:
            fs = self.get_filestorage()
            result = fs.get_data('user')
            m.assert_called_with('data_dir/user.dat', 'r')
            self.assertEqual(self.data, result)

    @patch('pycred.storages.file.create_secure_file')
    @patch('pycred.storages.file.check_file_security')
    def test_set_data(self, create_mock, check_mock):
        with patch('builtins.open', new_callable=mock_open) as m, patch('os.makedirs'):
            fs = self.get_filestorage()
            fs.set_data('user', self.data)
            m.assert_called_with('data_dir/user.dat', 'w')
            m().write.assert_called_with(self.data)

    def test_unset_data(self):
        with patch('os.unlink') as m:
            fs = self.get_filestorage()
            fs.unset_data('user')
            m.assert_called_with('data_dir/user.dat')

    @patch('pycred.storages.file.create_secure_file')
    @patch('pycred.storages.file.check_file_security')
    def test_delete(self, create_mock, check_mock):
        fs = self.get_filestorage()
        with patch('shutil.rmtree') as m, patch('os.path.isdir', return_value=True):
            fs.delete()
        m.assert_called_with('data_dir')

    @patch('pycred.storages.file.create_secure_file')
    @patch('pycred.storages.file.check_file_security')
    def test_get_data_raises_invaliduser_if_the_user_is_not_found(self, create_mock, check_mock):
        fs = self.get_filestorage()
        with self.assertRaises(InvalidUser):
            fs.get_data('user')

    @patch('pycred.storages.file.create_secure_file')
    @patch('pycred.storages.file.check_file_security')
    def test_get_data_raises_get_data_failed_for_permission_errors(self, create_mock, check_mock):
        with patch('builtins.open', side_effect=PermissionError()):
            fs = self.get_filestorage()
            with self.assertRaises(GetDataFailed):
                fs.get_data('user')

    @patch('pycred.storages.file.create_secure_file')
    @patch('pycred.storages.file.check_file_security')
    def test_set_data_raises_set_data_failed(self, create_mock, check_mock):
        fs = FileStorage('/invalid/random/path')
        with self.assertRaises(SetDataFailed):
            fs.set_data('user', self.data)

    def test_unset_data_raises_unset_data_failed(self):
        fs = FileStorage('data_dir')
        with patch('os.unlink', side_effect=PermissionError()):
            with self.assertRaises(UnsetDataFailed):
                fs.unset_data('user')

    def test_get_users(self):
        fs = self.get_filestorage()
        with patch('glob.glob', return_value=['data_dir/user2.dat', 'data_dir/user1.dat']):
            users = fs.get_users()
        self.assertEqual(['user1', 'user2'], users)

    def test_storage_file_created_with_correct_permissions(self):
        with tempfile.TemporaryDirectory(prefix='pycred-') as d:
            user = 'user'
            fs = FileStorage(d)
            path = fs.get_path(user)
            self.assertFalse(
                os.path.isfile(path), "Failed precondition, file '{path}' exists".format(path=path))
            fs.set_data(user, 'data')
            # Contains self-checks for permissions on creation.
            assert os.path.isfile(path)

    def test_storage_file_with_incorrect_permissions_raise_exception(self):
        with tempfile.TemporaryDirectory(prefix='pycred-') as d:
            user = 'user'
            fs = FileStorage(d)
            path = fs.get_path(user)
            self.assertFalse(
                os.path.isfile(path), "Failed precondition, file '{path}' exists".format(path=path))
            with open(path, 'w+'):
                pass
            with self.assertRaises(GetDataFailed):
                fs.get_data(user)
