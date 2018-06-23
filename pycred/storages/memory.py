from . import AbstractStorage, GetDataFailed, SetDataFailed


class MemoryStorage(AbstractStorage):

    def __init__(self):
        self.data = {}

    def get_data(self, user):
        try:
            return self.data[user]
        except Exception:
            raise GetDataFailed('MemoryStorage')

    def set_data(self, user, data):
        try:
            self.data[user] = data
        except Exception:
            raise SetDataFailed('FileStorage')
