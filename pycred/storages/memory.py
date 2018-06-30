import logging

from . import AbstractStorage, GetDataFailed, InvalidUser, SetDataFailed

logger = logging.getLogger('MemoryStorage')
logger.addHandler(logging.NullHandler())


class MemoryStorage(AbstractStorage):

    def __init__(self):
        self.data = {}

    def get_data(self, user):
        try:
            return self.data[user]
        except KeyError:
            raise InvalidUser('MemoryStorage') from None
        except Exception:
            raise GetDataFailed('MemoryStorage') from None

    def set_data(self, user, data):
        try:
            self.data[user] = data
        except Exception:
            raise SetDataFailed('FileStorage') from None

    def delete(self):
        logger.debug("Deleted")
