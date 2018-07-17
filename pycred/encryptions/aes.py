import logging
import os

from cryptography.fernet import Fernet

from . import AbstractEncryption
from ..fs import check_file_security, create_secure_directory, create_secure_file, \
    delete_unused_directory

logger = logging.getLogger('ClearEncryption')
logger.addHandler(logging.NullHandler())


class AesEncryption(AbstractEncryption):

    def __init__(self, key_path):
        self.key_path = os.path.expanduser(key_path)

    def encrypt(self, data):
        f = Fernet(self.get_key(self.key_path))
        encrypted_data = f.encrypt(data)
        return encrypted_data

    def decrypt(self, encrypted_data):
        f = Fernet(self.get_key(self.key_path))
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data

    def delete(self):
        if os.path.isfile(self.key_path):
            os.unlink(self.key_path)
            delete_unused_directory(os.path.dirname(self.key_path))
        logger.debug("Deleted")

    def get_key(self, key_path):
        if os.path.isfile(key_path):
            return self.read_key(key_path)
        else:
            return self.create_key(key_path)

    def read_key(self, key_path):
        with open(key_path, 'rb') as f:
            check_file_security(key_path)
            key = f.read()
        return key

    def create_key(self, key_path):
        key = Fernet.generate_key()
        create_secure_directory(os.path.dirname(key_path))
        create_secure_file(key_path)
        with open(key_path, 'wb+') as f:
            f.write(key)
        return key
