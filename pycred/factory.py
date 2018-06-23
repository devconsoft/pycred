from .encryptions.clear import ClearEncryption
from .serializers.json import JsonSerializer
from .storages.file import FileStorage
from .storages.memory import MemoryStorage
from .store import Store


class Factory(object):

    def get_serializer(self, backend_config):
        cls = self.get_serializer_class_from_name(backend_config.name)
        return cls(**backend_config.data)

    def get_storage(self, backend_config):
        cls = self.get_storage_class_from_name(backend_config.name)
        return cls(**backend_config.data)

    def get_encryption(self, backend_config):
        cls = self.get_encryption_class_from_name(backend_config.name)
        return cls(**backend_config.data)

    def get_store(self, store_config):
        name = store_config.name
        serializer = self.get_serializer(store_config.serializer)
        encryption = self.get_encryption(store_config.encryption)
        storage = self.get_storage(store_config.storage)
        return Store(name, serializer, encryption, storage)

    def get_serializer_class_from_name(self, name):
        return {'json': JsonSerializer}[name]

    def get_encryption_class_from_name(self, name):
        return {'clear': ClearEncryption}[name]

    def get_storage_class_from_name(self, name):
        return {'file': FileStorage, 'memory': MemoryStorage}[name]
