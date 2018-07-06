import logging

from pycred.storages import InvalidUser

logger = logging.getLogger('store')
logger.addHandler(logging.NullHandler())


class Store(object):

    def __init__(self, name, serializer, encryption, storage):
        self.name = name
        self.serializer = serializer
        self.encryption = encryption
        self.storage = storage
        serializer.store = self
        encryption.store = self
        storage.store = self

    def get_credentials(self, user):
        """Return credentials, or None if the user doesn't exist in the store."""
        try:
            encrypted_data = self.storage.get_data(user)
            data = self.encryption.decrypt(encrypted_data)
            credentials = self.serializer.deserialize(data)
        except InvalidUser:
            return None
        return credentials

    def set_credentials(self, user, credentials):
        data = self.serializer.serialize(credentials)
        encrypted_data = self.encryption.encrypt(data)
        self.storage.set_data(user, encrypted_data)

    def unset_credentials(self, user):
        self.storage.unset_data(user)

    def get_users(self):
        return self.storage.get_users()

    def delete(self):
        logger.debug("Deleting {name}".format(name=self.name))
        self.serializer.delete()
        self.encryption.delete()
        self.storage.delete()
