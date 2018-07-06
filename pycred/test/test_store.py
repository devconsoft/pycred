import unittest
from unittest.mock import MagicMock

from ..store import Store


class TestStore(unittest.TestCase):

    def test_store_sets_store_attribute_on_its_backends(self):
        storage = MagicMock()
        encryption = MagicMock()
        serializer = MagicMock()
        store = Store('name', serializer, encryption, storage)
        self.assertIs(storage.store, store)
        self.assertIs(encryption.store, store)
        self.assertIs(serializer.store, store)

    def test_get_credentials(self):
        credentials = MagicMock()
        storage = MagicMock()
        storage.get_data = MagicMock(return_value='encrypted_data')
        encryption = MagicMock()
        encryption.decrypt = MagicMock(return_value='data')
        serializer = MagicMock()
        serializer.deserialize = MagicMock(return_value=credentials)

        store = Store('name', serializer, encryption, storage)
        result = store.get_credentials('user')

        self.assertEqual(result, credentials)
        storage.get_data.assert_called_with('user')
        encryption.decrypt.assert_called_with('encrypted_data')
        serializer.deserialize.assert_called_with('data')

    def test_set_credentials(self):
        serializer = MagicMock()
        serializer.serialize = MagicMock(return_value='data')
        encryption = MagicMock()
        encryption.encrypt = MagicMock(return_value='encrypted_data')
        storage = MagicMock()
        credentials = MagicMock()

        store = Store('name', serializer, encryption, storage)
        store.set_credentials('user', credentials)

        serializer.serialize.assert_called_with(credentials)
        encryption.encrypt.assert_called_with('data')
        storage.set_data.assert_called_with('user', 'encrypted_data')

    def test_unset_credentials(self):
        serializer = MagicMock()
        encryption = MagicMock()
        storage = MagicMock()

        store = Store('name', serializer, encryption, storage)
        store.unset_credentials('user')
        storage.unset_data.assert_called_with('user')
        serializer.assert_not_called()
        encryption.assert_not_called()

    def test_delete(self):
        storage = MagicMock()
        encryption = MagicMock()
        serializer = MagicMock()
        store = Store('name', serializer, encryption, storage)
        store.delete()
        storage.delete.assert_called_once_with()
        encryption.delete.assert_called_once_with()
        serializer.delete.assert_called_once_with()

    def test_get_users(self):
        serializer = MagicMock()
        encryption = MagicMock()
        storage = MagicMock()
        storage.get_users = MagicMock(return_value=['user'])

        store = Store('name', serializer, encryption, storage)
        self.assertEqual(['user'], store.get_users())
