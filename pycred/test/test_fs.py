import os
import tempfile
import unittest

from ..fs import check_file_security, create_secure_file, delete_unused_directory


class TestFs(unittest.TestCase):

    def test_delete_unused_directory(self):
        with tempfile.TemporaryDirectory(prefix='pycred-') as d:
            path = os.path.join(d, 'a', 'b', 'c')
            file_to_be_deleted = os.path.join(path, 'file_to_be_deleted')
            file_to_be_saved = os.path.join(d, 'file_to_be_saved')
            os.makedirs(path)
            with open(file_to_be_deleted, 'w+'):
                pass
            with open(file_to_be_saved, 'w+'):
                pass
            self.assertTrue(os.path.isfile(file_to_be_saved))
            delete_unused_directory(path)
            self.assertTrue(os.path.isfile(file_to_be_saved))
            self.assertTrue(os.path.isdir(d))
            self.assertFalse(os.path.isdir(os.path.join(d, 'a', 'b')))
            self.assertFalse(os.path.isdir(os.path.join(d, 'a')))
            self.assertFalse(os.path.isfile(file_to_be_deleted))
            self.assertFalse(os.path.isdir(path))

    def test_create_check_secure_file(self):
        with tempfile.TemporaryDirectory(prefix='pycred-') as d:
            file_path = os.path.join(d, 'file')
            create_secure_file(file_path)
            check_file_security(file_path)
