from functools import lru_cache

from ruamel.yaml import YAML

from .paths import get_config_filepath, get_store_config_filename


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


DEFAULT_PYCRED_CONFIG = PyCredConfig(
    '~/.pycred/store', PyCredBackendDefaultConfig('json', BackendConfig('json', {})),
    PyCredBackendDefaultConfig('clear', BackendConfig('clear', {})),
    PyCredBackendDefaultConfig(
        'file', BackendConfig('file', {
            'path': '~/.pycred/data/storage/file'
        })))


@lru_cache(maxsize=1)
def get_pycred_config_file_parser():
    yaml = YAML(typ='unsafe')
    yaml.register_class(PyCredConfig)
    yaml.register_class(PyCredBackendDefaultConfig)
    yaml.register_class(BackendConfig)
    return yaml


@lru_cache(maxsize=1)
def get_store_config_file_parser():
    yaml = YAML(typ='unsafe')
    yaml.register_class(StoreConfig)
    yaml.register_class(BackendConfig)
    return yaml


def get_pycred_config():
    """
    Get PyCred configuration.

    :returns: PyCredConfig
    """
    path = get_config_filepath()
    parser = get_pycred_config_file_parser()
    with open(path, 'r') as f:
        result = parser.load(f)
        return result if result is not None else DEFAULT_PYCRED_CONFIG


def save_pycred_config(config):
    """
    Save PyCred configuration to file.

    :param config: PyCredConfig
    """
    path = get_config_filepath()
    parser = get_pycred_config_file_parser()
    with open(path, 'w') as f:
        parser.dump(config, f)


def get_store_config(store_config_dir, store_name):
    """
    Get Store configuration.

    :param store_config_dir: Path to store configurations directory.
    :returns: StoreConfig
    """
    parser = get_store_config_file_parser()
    path = get_store_config_filename(store_config_dir, store_name)
    with open(path, 'r') as f:
        return parser.load(f)


def save_store_config(store_config_dir, config):
    """
    Save store configuration to file.

    :param store_config_dir: Path to store configurations directory.
    :param config: StoreConfig
    """
    parser = get_store_config_file_parser()
    path = get_store_config_filename(store_config_dir, config.name)
    with open(path, 'w') as f:
        parser.dump(config, f)
