Configuration
=============

PyCred deals with two types of configuration:

* :ref:`PyCred Configuration`
* :ref:`Store Configuration`

PyCred Configuration
--------------------
This holds configuration options that are applicable for the entire pycred
installation. The configuration files is stored in the same directory as the
pycred python package.

* Path to directory where store configurations (``store_path``) are saved
* Default serializer backend for new stores
* Default encryption backend for new stores
* Default storage backend for new stores
* Initial/default configuration for the respective backends fore new stores

See also :ref:`PYCRED_CONFIG_FILE`.


Store Configuration
-------------------
Each store has its configuration saved in the ``store_path`` directory.
It holds the configuration for the backends used for that particular store.
Hence, it holds no credential data, only configuration about its backend.
The location of credential data is determine by the storage backend, and its
configuration for the particular store.

See also :ref:`PYCRED_STORE_PATH`.
