"""File system helper functions."""
import getpass
import os
import pwd
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
