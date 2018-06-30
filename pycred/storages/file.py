import logging
import os
import shutil

from . import AbstractStorage, GetDataFailed, InvalidUser, SetDataFailed

logger = logging.getLogger('FileStorage')
logger.addHandler(logging.NullHandler())


class FileStorage(AbstractStorage):

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def get_data(self, user):
        try:
            path = self.get_path(user)
            with open(path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise InvalidUser('FileStorage') from None
        except Exception as e:
            raise GetDataFailed('FileStorage') from None

    def set_data(self, user, data):
        try:
            path = self.get_path(user)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(data)
        except Exception:
            raise SetDataFailed('FileStorage') from None

    def get_path(self, user):
        return os.path.expanduser(os.path.join(self.data_dir, "{name}.dat".format(name=user)))

    def delete(self):
        path = self.data_dir
        if os.path.isdir(path):
            shutil.rmtree(path)
        logger.debug('Deleted')
