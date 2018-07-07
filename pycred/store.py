import logging

from pycred.storages import InvalidUser

logger = logging.getLogger('store')
logger.addHandler(logging.NullHandler())


class Store(object):

    def __init__(self, name, serializer, encryption, storage):
        """
        Store.

        :param name: Name of the store.
        :param serializer: Serializer backend instance.
        :param encryption: Encryption backend instance.
        :param storage: Storage backend instance.
        """
        self.name = name
        self.serializer = serializer
        self.encryption = encryption
        self.storage = storage
        serializer.store = self
        encryption.store = self
        storage.store = self

    def get_credentials(self, user):
        """
        Return credentials, or None if the user doesn't exist in the store.

        :param user: User
        :returns: Credentials
        """
        try:
            encrypted_data = self.storage.get_data(user)
            data = self.encryption.decrypt(encrypted_data)
            credentials = self.serializer.deserialize(data)
        except InvalidUser:
            return None
        return credentials

    def set_credentials(self, user, credentials):
        """
        Set (save) credentials for user.

        :param user: User
        :param credentials: Credentials
        """
        data = self.serializer.serialize(credentials)
        encrypted_data = self.encryption.encrypt(data)
        self.storage.set_data(user, encrypted_data)

    def unset_credentials(self, user):
        """
        Unset (remove) credentials for user.

        :param user: User
        """
        self.storage.unset_data(user)

    def get_users(self):
        """
        Return a list of all users that have credentials in the store.

        :returns: List of users
        """
        return self.storage.get_users()

    def delete(self):
        """Delete the store and all associated configuration and stored credentials."""
        logger.debug("Deleting {name}".format(name=self.name))
        self.serializer.delete()
        self.encryption.delete()
        self.storage.delete()
