import glob
import logging
import os

from . import AbstractStorage, GetDataFailed, InvalidUser, SetDataFailed, UnsetDataFailed
from ..fs import InvalidFilePermissions, check_file_security, create_secure_directory, \
    create_secure_file, delete_unused_directory

logger = logging.getLogger('FileStorage')
logger.addHandler(logging.NullHandler())


class FileStorage(AbstractStorage):

    def __init__(self, data_dir):
        self.data_dir = os.path.expanduser(data_dir)

    def get_data(self, user):
        try:
            path = self.get_path(user)
            check_file_security(path)
            with open(path, 'rb') as f:
                return f.read()
        except InvalidFilePermissions as e:
            logger.error(str(e))
            raise GetDataFailed('FileStorage') from None
        except FileNotFoundError:
            raise InvalidUser('FileStorage') from None
        except Exception as e:
            raise GetDataFailed('FileStorage') from None

    def set_data(self, user, data):
        try:
            path = self.get_path(user)
            if not os.path.isfile(path):
                create_secure_directory(os.path.dirname(path))
                create_secure_file(path)

            check_file_security(path)

            with open(path, 'wb') as f:
                f.write(data)
        except InvalidFilePermissions as e:
            logger.error(str(e))
            raise SetDataFailed('FileStorage') from None
        except Exception:
            raise SetDataFailed('FileStorage') from None

    def unset_data(self, user):
        try:
            path = self.get_path(user)
            os.unlink(path)
        except Exception:
            raise UnsetDataFailed('FileStorage') from None

    def get_path(self, user):
        return os.path.join(self.data_dir, "{name}.dat".format(name=user))

    def delete(self):
        delete_unused_directory(self.data_dir)
        logger.debug('Deleted')

    def get_users(self):
        files = glob.glob(os.path.join(self.data_dir, '*.dat'))
        result = [os.path.basename(f).rsplit('.', 1)[0] for f in files]
        return sorted(result)
