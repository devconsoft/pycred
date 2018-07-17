"""File system helper functions."""
import errno
import getpass
import os
import pwd
import shutil
import stat

SECURE_FILE_MODE = stat.S_IRUSR | stat.S_IWUSR


class InvalidFilePermissions(Exception):

    def __init__(self, path, ex_mode, ex_owner, ac_mode, ac_owner):
        msg = 'Invalid permissions or owner for file, path={path}. '\
                'Expected mode={ex_mode}, owner={ex_owner}. Actual mode={ac_mode}, owner={ac_owner}'.format(
                    path=path, ex_mode=ex_mode, ex_owner=ex_owner, ac_mode=ac_mode, ac_owner=ac_owner)
        super().__init__(msg)


def create_secure_file(path):
    """
    Create an empty file at path, only accessable by user.

    If the file exists, it will be truncated and its access rights changed.

    :param path: Path to file.
    """
    with open(path, 'wb+'):
        pass
    os.chmod(path, mode=SECURE_FILE_MODE)


def check_file_security(path):
    """
    Check file permissions and owner.

    :param path: Path to file.
    """
    mode = stat.S_IMODE(os.stat(path).st_mode)
    user = getpass.getuser()
    owner = pwd.getpwuid(os.stat(path).st_uid).pw_name
    if mode != SECURE_FILE_MODE or user != owner:
        raise InvalidFilePermissions(path, SECURE_FILE_MODE, user, mode, owner)


def create_secure_directory(path):
    """
    Create directory(s) only accessable by user.

    Non-existing parent-directories will also be created.
    It is okay if the directory already exists.

    :param path: Path to directory
    """
    os.makedirs(path, mode=0o700, exist_ok=True)


def delete_unused_directory(path):
    """
    Delete directory, and all its content, and all un-used parent directories.

    The specified directory must exist in order for its parent directories to be deleted.
    Exception can be raised if the user has unsufficied privileges or if deletetion
    otherwise failes.

    :param path: Path to directory
    """
    if os.path.isdir(path):
        shutil.rmtree(path)
        while True:
            try:
                path = os.path.dirname(path)
                os.rmdir(path)
            except OSError as e:
                if e.errno == errno.ENOTEMPTY:
                    break
                else:
                    raise
