import getpass
import glob
import logging
import os

from .config import ConfigurationManager
from .credentials import Credentials
from .exceptions import StoreAlreadyExists
from .factory import Factory

logger = logging.getLogger('pycred')
logger.addHandler(logging.NullHandler())


class PyCred(object):

    def __init__(self):
        self.config = ConfigurationManager()
        self.factory = Factory()

    def get_store(self, name):
        """
        Get existing store based on name.

        :param name: name of store to retrieve.
        :return: Store
        """
        store_config = self.config.get_store_config(name)
        return self.factory.get_store(store_config)

    def init_store(self, name, serializer, encryption, storage):
        """
        Initialize a new store, and save the configuration.

        The function returns the new store instance.

        If a store with the same name already exists, an StoreAlreadyExists exception
        is thrown.

        :param name: Name of the store.
        :param serializer: Name of the serializer type.
        :param encryption: Name of the encryption type.
        :param storage: Name of the storage type.
        :returns: Store
        """
        if name in self.get_store_names():
            raise StoreAlreadyExists(name)
        store_config = self.config.create_store_config(name, serializer, encryption, storage)
        self.config.save_store_config(store_config)
        store = self.factory.get_store(store_config)
        return store

    def delete_store(self, name):
        """
        Delete a store, its configuration and all its data.

        :param name: Name of the store to delete.
        """
        logger.info("Deleting store {name}".format(name=name))
        logger.debug("delete_store (store_path={sp})".format(sp=self.get_config().get_store_path()))
        store_configfile = self.config.get_store_config_filename(name)
        store_config = self.config.get_store_config(name)
        logger.debug("delete_store (store_configfile={sc})".format(sc=store_configfile))
        store = self.factory.get_store(store_config)
        store.delete()
        os.remove(store_configfile)

    def get_config(self):
        """
        Get pycred configuration.

        :returns: PyCredConfig
        """
        return self.config.get_pycred_config()

    def get_store_names(self):
        """Get the names of all stores as a list of strings."""
        store_path = self.get_config().get_store_path()
        logger.debug("get_store_names (store_path={sp})".format(sp=store_path))
        files = glob.glob(os.path.join(store_path, '*.yaml'))
        result = [os.path.basename(f).rsplit('.', 1)[0] for f in files]
        return sorted(result)

    def get_default_user(self):
        return getpass.getuser()

    def set_credentials(self, store, username, password, user=None):
        if user is None:
            user = self.get_default_user()
        store = self.get_store(store)
        store.set_credentials(user, Credentials(username, password))

    def get_credentials(self, store, user=None):
        """
        Get credential from store for the specified user.

        If the user doesn't exist in the store, None is returned.

        :param store: Name of store
        :param user: User
        :returns: Credentials or None if the user doesn't exist in the store.
        """

        if user is None:
            user = self.get_default_user()
        store = self.get_store(store)
        return store.get_credentials(user)
