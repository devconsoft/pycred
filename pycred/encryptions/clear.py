import logging

from . import AbstractEncryption

logger = logging.getLogger('ClearEncryption')
logger.addHandler(logging.NullHandler())


class ClearEncryption(AbstractEncryption):

    def encrypt(self, data):
        return data

    def decrypt(self, encrypted_data):
        return encrypted_data

    def delete(self):
        logger.debug("Deleted")
