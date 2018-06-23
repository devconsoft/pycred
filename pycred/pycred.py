from .config import get_pycred_config, get_store_config
from .factory import Factory


def get_store(name):
    """
    Get credentials-store.

    :param name: name of store to retrieve.
    :return: Store
    """
    pycred_config = get_pycred_config()
    store_config = get_store_config(pycred_config.store_path, name)
    factory = Factory()
    return factory.get_store(store_config)
