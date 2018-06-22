from . import AbstractEncryption


class ClearEncryption(AbstractEncryption):

    def encrypt(self, data):
        return data

    def decrypt(self, encrypted_data):
        return encrypted_data
