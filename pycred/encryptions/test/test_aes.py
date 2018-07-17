import os
import tempfile
import unittest

from ..aes import AesEncryption


class TestAesEncryption(unittest.TestCase):

    data = b'data'

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory(prefix='pycred-')
        self.ws = self.tmpdir.__enter__()
        self.key_dir = os.path.join(self.ws, 'keys')
        self.key_path = os.path.join(self.key_dir, 'key.aes')
        self.enc = AesEncryption(self.key_path)

    def tearDown(self):
        self.tmpdir.__exit__(None, None, None)
        self.enc = None
        self.ws = None

    def test_get_key_creates_keyfile_and_keydir_if_it_does_not_exist(self):
        key = self.enc.get_key(self.key_path)
        self.assertIsNotNone(key)
        self.assertTrue(os.path.isfile(self.key_path))

    def test_delete_deletes_key_file_and_unused_dir(self):
        with open(os.path.join(self.ws, 'blocking_file'), 'w+'):
            pass
        self.enc.get_key(self.key_path)
        self.enc.delete()
        self.assertFalse(os.path.isfile(self.key_path))
        self.assertFalse(os.path.isdir(self.key_dir))
        self.assertTrue(os.path.isdir(self.ws))

    def test_encrypt_decrypt_with_pre_existing_key(self):
        self.enc.get_key(self.key_path)
        encrypted_data = self.enc.encrypt(self.data)
        self.assertNotEqual(self.data, encrypted_data)

        data = self.enc.decrypt(encrypted_data)
        self.assertEqual(self.data, data)

    def test_encrypt_decrypt_without_existing_key(self):
        encrypted_data = self.enc.encrypt(self.data)
        self.assertNotEqual(self.data, encrypted_data)

        data = self.enc.decrypt(encrypted_data)
        self.assertEqual(self.data, data)
