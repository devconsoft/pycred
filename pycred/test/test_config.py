import unittest
from io import StringIO
from textwrap import dedent
from unittest.mock import MagicMock, mock_open, patch

from ..config import BackendConfig, ConfigurationManager, DEFAULT_PYCRED_CONFIG, \
    PyCredBackendDefaultConfig, PyCredConfig, StoreConfig


class TestPyCredBackendDefaultConfig(unittest.TestCase):

    def setUp(self):
        self.backend1 = BackendConfig('BE1', {})
        self.backend2 = BackendConfig('BE2', {})
        self.config = PyCredBackendDefaultConfig('BE1', [self.backend1, self.backend2])

    def test_get_backend_using_default(self):
        result = self.config.get_backend(None)
        self.assertIs(result, self.backend1)

    def test_get_backend_using_name(self):
        result = self.config.get_backend('BE2')
        self.assertIs(result, self.backend2)

    def test_get_backend_names(self):
        result = self.config.get_backend_names()
        self.assertEqual(['BE1', 'BE2'], result)


class TestPyCred(unittest.TestCase):

    def test_get_store_path_expands_user(self):
        config = PyCredConfig('~/dir', None, None, None)
        self.assertNotIn('~', config.get_store_path())

    def test_store_path_can_be_overridden_by_env(self):
        with patch.dict('os.environ', {'PYCRED_STORE_PATH': 'overridden'}):
            config = PyCredConfig('store_path', None, None, None)
            self.assertEqual(config.get_store_path(), 'overridden')


class TestConfigurationManager(unittest.TestCase):

    maxDiff = None

    pycred = dedent(
        """\
        ---
        !PyCredConfig
        encryptions: !PyCredBackendDefaultConfig
          default: DEFAULT
          backends:
          - !BackendConfig
            name: mybackend
            data:
              key: VALUE
        serializer: !PyCredBackendDefaultConfig
          default: DEFAULT
          backends:
          - !BackendConfig
            name: mybackend
            data:
              key: VALUE
        storages: !PyCredBackendDefaultConfig
          default: DEFAULT
          backends:
          - !BackendConfig
            name: mybackend
            data:
              key: VALUE
        store_path: STORE_PATH
        """)

    store = dedent(
        """\
        ---
        !StoreConfig
        name: STORE
        encryptions: !BackendConfig
          name: ENCRYPTION
          data:
            key: VALUE
        serializer: !BackendConfig
          name: SERIALIZER
          data:
            key: VALUE
        storage: !BackendConfig
          name: STORAGE
          data:
            key: VALUE
        """)

    def get_default_config(self):
        encryptions = PyCredBackendDefaultConfig('EN', [BackendConfig('EN', {})])
        serializers = PyCredBackendDefaultConfig('SE', [BackendConfig('SE', {})])
        storages = PyCredBackendDefaultConfig('ST', [BackendConfig('ST', {})])
        return PyCredConfig('store_path', serializers, encryptions, storages)

    def test_get_pycred_config(self):
        with patch('builtins.open', new_callable=mock_open, read_data=self.pycred):
            result = ConfigurationManager().get_pycred_config()
        self.assertIsInstance(result, PyCredConfig)
        self.assertEqual('STORE_PATH', result.store_path)
        storages = result.storages
        self.assertEqual('DEFAULT', storages.default)
        backend = storages.backends[0]
        self.assertEqual('mybackend', backend.name)
        self.assertIsInstance(backend.data, dict)
        self.assertEqual('VALUE', backend.data['key'])

    def test_save_pycred_config(self):
        config = self.get_default_config()
        f = StringIO()

        with patch('builtins.open', new_callable=mock_open) as m:
            m().__enter__ = MagicMock(return_value=f)
            ConfigurationManager().save_pycred_config(config)

        result = f.getvalue()
        expected = dedent(
            """\
            !PyCredConfig
            encryptions: !PyCredBackendDefaultConfig
              backends:
              - !BackendConfig
                data: {}
                name: EN
              default: EN
            serializers: !PyCredBackendDefaultConfig
              backends:
              - !BackendConfig
                data: {}
                name: SE
              default: SE
            storages: !PyCredBackendDefaultConfig
              backends:
              - !BackendConfig
                data: {}
                name: ST
              default: ST
            store_path: store_path
            """)  # noqa
        self.assertEqual(expected, result)

    def test_get_store_config(self):
        with patch('builtins.open', new_callable=mock_open, read_data=self.store) as m, \
                patch.object(ConfigurationManager, 'get_pycred_config', return_value=self.get_default_config()):
            result = ConfigurationManager().get_store_config('store')
        m.assert_called_with('store_path/store.yaml', 'r')
        self.assertIsInstance(result, StoreConfig)
        self.assertEqual('STORE', result.name)
        storage = result.storage
        self.assertEqual('STORAGE', storage.name)
        data = storage.data
        self.assertIsInstance(data, dict)
        self.assertEqual('VALUE', data['key'])

    def test_save_store_config(self):
        serializer = BackendConfig('BE', {})
        encryption = BackendConfig('BE', {})
        storage = BackendConfig('BE', {})
        config = StoreConfig('store', serializer, encryption, storage)
        f = StringIO()

        with patch('builtins.open', new_callable=mock_open) as m, \
                patch.object(ConfigurationManager, 'get_pycred_config', return_value=self.get_default_config()):
            m().__enter__ = MagicMock(return_value=f)
            ConfigurationManager().save_store_config(config)

        m.assert_called_with('store_path/store.yaml', 'w')
        result = f.getvalue()
        expected = dedent(
            """\
            !StoreConfig
            encryption: !BackendConfig
              data: {}
              name: BE
            name: store
            serializer: !BackendConfig
              data: {}
              name: BE
            storage: !BackendConfig
              data: {}
              name: BE
            """)  # noqa
        self.assertEqual(expected, result)

    def test_create_store_config(self):
        pycred_config = self.get_default_config()
        with patch.object(ConfigurationManager, 'get_pycred_config', return_value=pycred_config):
            store_config = ConfigurationManager().create_store_config('store', None, None, None)

        self.assertEqual('store', store_config.name)
        self.assertEqual('SE', store_config.serializer.name)
        self.assertEqual('EN', store_config.encryption.name)
        self.assertEqual('ST', store_config.storage.name)

    def test_macro_expand_file_config(self):
        cfg = DEFAULT_PYCRED_CONFIG.storages.get_backend('file')
        tokens = {'%store%': 'STORE'}
        cfg = ConfigurationManager().macro_expand(cfg, tokens)
        self.assertEqual(cfg.data['data_dir'], '~/.pycred/data/STORE/storage/file')
