import getpass
import glob
import logging
import os
import pwd
import shutil
import stat

from . import AbstractStorage, GetDataFailed, InvalidUser, SetDataFailed, UnsetDataFailed

logger = logging.getLogger('FileStorage')
logger.addHandler(logging.NullHandler())


class FileStorage(AbstractStorage):

    def __init__(self, data_dir):
        self.data_dir = os.path.expanduser(data_dir)

    def get_data(self, user):
        try:
            path = self.get_path(user)
            self._check_file_security(path)
            with open(path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise InvalidUser('FileStorage') from None
        except Exception as e:
            raise GetDataFailed('FileStorage') from None

    def set_data(self, user, data):
        try:
            path = self.get_path(user)
            os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
            if not os.path.isfile(path):
                self._create_secure_file(path)

            self._check_file_security(path)

            with open(path, 'w') as f:
                f.write(data)
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
        path = self.data_dir
        if os.path.isdir(path):
            shutil.rmtree(path)
        logger.debug('Deleted')

    def get_users(self):
        files = glob.glob(os.path.join(self.data_dir, '*.dat'))
        result = [os.path.basename(f).rsplit('.', 1)[0] for f in files]
        return sorted(result)

    def _create_secure_file(self, path):
        """
        Create file at path, only accessable by user.

        :param path: Path to file.
        """
        with open(path, 'w'):
            pass
        os.chmod(path, mode=(stat.S_IRUSR | stat.S_IWUSR))

    def _check_file_security(self, path):
        """
        Check file permissions and owner.

        :param path: Path to file.
        """
        mode = stat.S_IMODE(os.stat(path).st_mode)
        user = getpass.getuser()
        owner = pwd.getpwuid(os.stat(path).st_uid).pw_name
        if mode != (stat.S_IRUSR | stat.S_IWUSR) or user != owner:
            logger.debug(
                'mode={mode}, user={user}, owner={owner}'.format(mode=mode, user=user, owner=owner))
            logger.error('Invalid permissions of storage file (path={path})'.format(path=path))
            raise Exception('Insecure file permissions')
