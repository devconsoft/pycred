import os
import tempfile
import unittest
from unittest.mock import patch

from ..config import DEFAULT_PYCRED_CONFIG, BackendConfig, StoreConfig
from ..credentials import Credentials
from ..encryptions.clear import ClearEncryption
from ..exceptions import StoreAlreadyExists, StoreDoesNotExist
from ..pycred import PyCred
from ..serializers.json import JsonSerializer
from ..storages.file import FileStorage


class TestPyCred(unittest.TestCase):

    def test_get_json_clear_memory_store(self):
        serializer = BackendConfig('json', {})
        encryption = BackendConfig('clear', {})
        storage = BackendConfig('memory', {})
        store_config = StoreConfig('store', serializer, encryption, storage)
        with patch('pycred.config.ConfigurationManager.get_store_config',
                   return_value=store_config):
            user = 'user'
            cred = Credentials('USERNAME', 'PASSWORD')
            store = PyCred().get_store('store')
            store.set_credentials(user, cred)
            result = store.get_credentials(user)
            self.assertEqual(cred.username, result.username)
            self.assertEqual(cred.password, result.password)

    def test_init_json_clear_file_store(self):
        with patch('pycred.config.ConfigurationManager.get_pycred_config', return_value=DEFAULT_PYCRED_CONFIG), \
                patch('pycred.config.ConfigurationManager.save_store_config'):
            store = PyCred().init_store('store', 'json', 'clear', 'file')

        self.assertIsInstance(store.serializer, JsonSerializer)
        self.assertIsInstance(store.encryption, ClearEncryption)
        self.assertIsInstance(store.storage, FileStorage)
        default_path = DEFAULT_PYCRED_CONFIG.storages.get_backend('file').data['data_dir']
        self.assertEqual(default_path, store.storage.data_dir)

    def test_get_store_names(self):
        with tempfile.TemporaryDirectory(prefix='pycred-') as d:
            with open(os.path.join(d, "s1.yaml"), 'w+'):
                pass
            with open(os.path.join(d, "s2.yaml"), 'w+'):
                pass
            with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
                names = PyCred().get_store_names()

        self.assertEqual(['s1', 's2'], names)

    def test_init_already_existing_store_raises_exception(self):
        with patch('pycred.pycred.PyCred.get_store_names', return_value='store'):
            with self.assertRaises(StoreAlreadyExists):
                PyCred().init_store('store', None, None, None)

    def test_get_store_that_does_not_exists_raises_exception(self):
        with tempfile.TemporaryDirectory(prefix='pycred-') as d:
            with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
                with self.assertRaises(StoreDoesNotExist):
                    PyCred().get_store('non-existing-store')

    def test_delete_store_that_does_not_exists_raises_exception(self):
        with tempfile.TemporaryDirectory(prefix='pycred-') as d:
            with patch.dict('os.environ', {'PYCRED_STORE_PATH': d}):
                with self.assertRaises(StoreDoesNotExist):
                    PyCred().delete_store('non-existing-store')
