import os

from . import AbstractStorage, GetDataFailed, SetDataFailed


class FileStorage(AbstractStorage):

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def get_data(self, user):
        try:
            path = self.get_path(user)
            with open(path, 'r') as f:
                return f.read()
        except Exception:
            raise GetDataFailed('FileStorage')

    def set_data(self, user, data):
        try:
            path = self.get_path(user)
            with open(path, 'w') as f:
                f.write(data)
        except Exception:
            raise SetDataFailed('FileStorage')

    def get_path(self, user):
        return os.path.join(self.data_dir, "{name}.dat".format(name=user))
