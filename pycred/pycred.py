from .factory import Factory
from .store import Store

def get_store(name):
    """
    Get credentials-store.

    :param name: name of store to retrieve.
    :return: Store
    """
    factory = Factory()
    storage = factory.get_storage()
    encryption = factory.get_encryption()
    serializer = factory.get_serializer()
    store = Store(serializer, encryption, storage)
    return store
