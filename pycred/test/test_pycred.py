import unittest
from unittest.mock import patch

from ..config import BackendConfig, StoreConfig
from ..credentials import Credentials
from ..pycred import get_store


class TestPyCredLib(unittest.TestCase):

    def test_get_json_clear_memory_store(self):
        serializer = BackendConfig('json', {})
        encryption = BackendConfig('clear', {})
        storage = BackendConfig('memory', {})
        store_config = StoreConfig('store', serializer, encryption, storage)
        with patch('pycred.pycred.get_pycred_config'), \
                patch('pycred.pycred.get_store_config', return_value=store_config):
            user = 'user'
            cred = Credentials('USERNAME', 'PASSWORD')
            store = get_store('store')
            store.set_credentials(user, cred)
            result = store.get_credentials(user)
            self.assertEqual(cred.username, result.username)
            self.assertEqual(cred.password, result.password)
