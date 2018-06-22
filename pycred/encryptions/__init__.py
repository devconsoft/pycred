from abc import ABCMeta, abstractmethod


class DecryptionFailed(Exception):
    """Thrown if data passed to encryption could not be decrypted."""
    pass


class EncryptionFailed(Exception):
    """Thrown if data passed to encryption could not be encrypted."""
    pass


class AbstractEncryption(metaclass=ABCMeta):

    @abstractmethod
    def encrypt(self, data):
        """
        Encrypt data.

        If encryption fails, the method should throw EncryptionFailed exception.

        The exception is not allowed to contain any data except the name of
        the ecnryption class.
        """
        pass

    @abstractmethod
    def decrypt(self, encrypted_data):
        """
        Decrypt encrypted data to clear.

        If decryption fails, the method should throw DecryptionFailed exception.

        The exception is not allowed to contain any data except the name of
        the ecnryption class.
        """
        pass
