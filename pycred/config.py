import os
from functools import lru_cache

from ruamel.yaml import YAML

from .paths import get_config_filepath


class BackendConfig(object):

    def __init__(self, name, data):
        """
        Store backend configuration.

        It holds configuration for a specific backend as it is configured for a
        store instance.

        :param name: Name of backend
        :param data: Dict of the settings to use when initializing the backend.
        """
        self.name = name
        self.data = data


class StoreConfig(object):

    def __init__(self, name, serializer, encryption, storage):
        """
        Store configuration.

        It holds the configuration for a store instance.

        :param name: Name of store
        :param serializer: BackendConfig for the serializer.
        :param encryption: BackendConfig for the encryption.
        :param storage: BackendConfig for the storage.
        """
        self.name = name
        self.serializer = serializer
        self.encryption = encryption
        self.storage = storage


class PyCredBackendDefaultConfig(object):

    def __init__(self, default, backends):
        """
        Pycred Backend Default Configuration.

        It holds the name of the default backend of the particular backend type,
        and a list of the configurations that should be used by default for the
        various backends of that type.

        :param default: Name of the default backend of this type.
        :param backends: List of BackendConfigs.
        """
        self.default = default
        self.backends = backends

    def get_backend(self, name):
        """
        Get backend by name; returns None if not found.

        If name is None, default is used as name.

        :param name: Name of backend to retrieve.
        :returns: BackendConfig
        """
        result = None
        if name is None:
            name = self.default

        for be in self.backends:
            if be.name == name:
                result = be
                break
        return result

    def get_backend_names(self):
        return [be.name for be in self.backends]


class PyCredConfig(object):

    def __init__(self, store_path, serializers, encryptions, storages):
        """
        Pycred Configuration.

        It holds the pycred library configuration.

        :param store_path: Path to where individual store configurations are saved.
        :param serializers: PyCredBackendDefaultConfig for serializers.
        :param encryptions: PyCredBackendDefaultConfig for encryptions.
        :param storages: PyCredBackendDefaultConfig for storages.
        """
        self.store_path = store_path
        self.serializers = serializers
        self.encryptions = encryptions
        self.storages = storages

    def get_store_path(self):
        path = os.environ.get('PYCRED_STORE_PATH', self.store_path)
        return os.path.expanduser(path)


DEFAULT_PYCRED_CONFIG = PyCredConfig(
    '~/.pycred/store', PyCredBackendDefaultConfig('json', [BackendConfig('json', {})]),
    PyCredBackendDefaultConfig('clear', [BackendConfig('clear', {})]),
    PyCredBackendDefaultConfig(
        'file', [
            BackendConfig('file', {
                'data_dir': '~/.pycred/data/storage/file'
            }),
            BackendConfig('memory', {})
        ]))


class ConfigurationManager(object):

    @lru_cache(maxsize=1)
    def get_pycred_config_file_parser(self):
        yaml = YAML(typ='unsafe')
        yaml.register_class(PyCredConfig)
        yaml.register_class(PyCredBackendDefaultConfig)
        yaml.register_class(BackendConfig)
        return yaml

    @lru_cache(maxsize=1)
    def get_store_config_file_parser(self):
        yaml = YAML(typ='unsafe')
        yaml.register_class(StoreConfig)
        yaml.register_class(BackendConfig)
        return yaml

    def get_pycred_config(self):
        """
        Get PyCred configuration.

        :returns: PyCredConfig
        """
        path = get_config_filepath()
        parser = self.get_pycred_config_file_parser()
        with open(path, 'r') as f:
            result = parser.load(f)
            return result if result is not None else DEFAULT_PYCRED_CONFIG

    def save_pycred_config(self, config):
        """
        Save PyCred configuration to file.

        :param config: PyCredConfig
        """
        path = get_config_filepath()
        parser = self.get_pycred_config_file_parser()
        with open(path, 'w') as f:
            parser.dump(config, f)

    def get_store_config(self, store_name):
        """
        Get Store configuration.

        :param store_config_dir: Path to store configurations directory.
        :returns: StoreConfig
        """
        parser = self.get_store_config_file_parser()
        path = self.get_store_config_filename(store_name)
        with open(path, 'r') as f:
            return parser.load(f)

    def save_store_config(self, config):
        """
        Save store configuration to file.

        :param store_config_dir: Path to store configurations directory.
        :param config: StoreConfig
        """
        parser = self.get_store_config_file_parser()
        path = self.get_store_config_filename(config.name)
        with open(path, 'w') as f:
            parser.dump(config, f)

    def create_store_config(self, name, serializer, encryption, storage):
        """
        Create a StoreConfig instance, using provided backend names and pycred defaults.

        :param name: Name of the store.
        :param serializer: Name of the serializer type.
        :param encryption: Name of the encryption type.
        :param storage: Name of the storage type.
        :returns: StoreConfig
        """
        pycred_config = self.get_pycred_config()
        serializer_config = pycred_config.serializers.get_backend(serializer)
        encryption_config = pycred_config.encryptions.get_backend(encryption)
        storage_config = pycred_config.storages.get_backend(storage)
        return StoreConfig(name, serializer_config, encryption_config, storage_config)

    def get_store_config_filename(self, store_name):
        store_config_dir = self.get_pycred_config().get_store_path()
        return os.path.join(store_config_dir, "{name}.yaml".format(name=store_name))
