import logging

from . import AbstractStorage, GetDataFailed, SetDataFailed

logger = logging.getLogger('MemoryStorage')
logger.addHandler(logging.NullHandler())


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

    def delete(self):
        logger.debug("Deleted")
