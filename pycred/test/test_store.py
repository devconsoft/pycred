import unittest
from unittest.mock import MagicMock

from ..store import Store


class TestStore(unittest.TestCase):

    def test_get_credentials(self):
        storage = MagicMock()
        storage.get_data = MagicMock(return_value='encrypted_data')
        encryption = MagicMock()
        encryption.decrypt = MagicMock(return_value='data')
        serializer = MagicMock()
        serializer.deserialize = MagicMock(return_value='credentials')

        store = Store(serializer, encryption, storage)
        credentials = store.get_credentials('user')

        self.assertEqual(credentials, 'credentials')
        storage.get_data.assert_called_with('user')
        encryption.decrypt.assert_called_with('encrypted_data')
        serializer.deserialize.assert_called_with('data')
