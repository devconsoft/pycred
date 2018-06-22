class Store(object):

    def __init__(self, serializer, encryption, storage):
        self.serializer = serializer
        self.encryption = encryption
        self.storage = storage

    def get_credentials(self, user):
        encrypted_data = self.storage.get_data(user)
        data = self.encryption.decrypt(encrypted_data)
        credentials = self.serializer.deserialize(data)
        return credentials
