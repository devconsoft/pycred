import unittest

from ..clear import ClearEncryption


class TestClearEncryption(unittest.TestCase):

    data = 'data'

    def test_encrypt_keeps_data_clear(self):
        e = ClearEncryption()
        result = e.encrypt(self.data)
        self.assertEqual(self.data, result)

    def test_decrypt_returns_same_data(self):
        e = ClearEncryption()
        result = e.decrypt(self.data)
        self.assertEqual(self.data, result)
