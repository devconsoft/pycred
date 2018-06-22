from .encryptions.clear import ClearEncryption
from .serializers.json import JsonSerializer
from .storages.file import FileStorage


class Factory(object):

    def get_serializer(self):
        return JsonSerializer()

    def get_storage(self):
        return FileStorage('~/.pycred/data/storage/filestorage')

    def get_encryption(self):
        return ClearEncryption()
