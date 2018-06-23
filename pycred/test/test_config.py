import unittest
from io import StringIO
from textwrap import dedent
from unittest.mock import MagicMock, mock_open, patch

from ..config import BackendConfig, PyCredBackendDefaultConfig, PyCredConfig, StoreConfig, \
    get_pycred_config, get_store_config, save_pycred_config, save_store_config


class TestConfig(unittest.TestCase):

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

    def test_get_pycred_config(self):
        with patch('builtins.open', new_callable=mock_open, read_data=self.pycred):
            result = get_pycred_config()
        self.assertIsInstance(result, PyCredConfig)
        self.assertEqual('STORE_PATH', result.store_path)
        storages = result.storages
        self.assertEqual('DEFAULT', storages.default)
        backend = storages.backends[0]
        self.assertEqual('mybackend', backend.name)
        self.assertIsInstance(backend.data, dict)
        self.assertEqual('VALUE', backend.data['key'])

    def test_save_pycred_config(self):
        encryptions = PyCredBackendDefaultConfig('default', [BackendConfig('BE', {})])
        serializers = PyCredBackendDefaultConfig('default', [BackendConfig('BE', {})])
        storages = PyCredBackendDefaultConfig('default', [BackendConfig('BE', {})])
        config = PyCredConfig('store_path', serializers, encryptions, storages)
        f = StringIO()

        with patch('builtins.open', new_callable=mock_open) as m:
            m().__enter__ = MagicMock(return_value=f)
            save_pycred_config(config)

        result = f.getvalue()
        expected = dedent(
            """\
            !PyCredConfig
            encryptions: !PyCredBackendDefaultConfig
              backends:
              - !BackendConfig
                data: {}
                name: BE
              default: default
            serializers: !PyCredBackendDefaultConfig
              backends:
              - !BackendConfig
                data: {}
                name: BE
              default: default
            storages: !PyCredBackendDefaultConfig
              backends:
              - !BackendConfig
                data: {}
                name: BE
              default: default
            store_path: store_path
            """)  # noqa
        self.assertEqual(expected, result)

    def test_get_store_config(self):
        with patch('builtins.open', new_callable=mock_open, read_data=self.store) as m:
            result = get_store_config('dir', 'store')
        m.assert_called_with('dir/store.yaml', 'r')
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

        with patch('builtins.open', new_callable=mock_open) as m:
            m().__enter__ = MagicMock(return_value=f)
            save_store_config('dir', config)

        m.assert_called_with('dir/store.yaml', 'w')
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
