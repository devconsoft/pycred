********
Overview
********


.. uml:: overview.pu


Data-flow
---------
When an application uses pycred it requests the credentials using a credential-store
name and a username (that defaults to the current user).
The retrieved data-set contain a single username-password pair.

The store is configured to use a specific serializer, storage and encryption backend.
When a store is loaded, pycred reads the data from storage, using the stores
storage configuration. The read data is passed for decryption to the
encryption backend, before deserialized by the serializer-backend and return in the form
of a credentials object.


.. uml:: dataflow.pu


Configuration
-------------
Configuration is stored together with the pycred application.
If pycred is centrally installed, changing the configuration will require
the same privileges as when the installation was made.

The pycred configuration handles:
 * default serializer
 * default storage
 * default encryption
 * default configuration for each serializer backend
 * default configuration for each storage backend
 * default configuration for each encryption backend
 * location of store configuration, usually relative to the system user
   so that the user can manage its credentials without extended privileges.


Credential-Stores
-----------------
PyCred groups its data into credential-stores. A store uses a specified
serializer backend, storage backend and encryption backend.

When using the pycred library, an application will request
the credentials for a particular credential-store for a particular user.

A credential-store only holds one username-password pair per user.
This to ensure the credentials are unambiguous for the given context.

The system username might be different than the username in the credentials.
To allow for a central credential-store used by many users, the user
is mapped to a username-password pair in the store.

When creating a new store, the default serializer, storage and encryption backends will be
used unless otherwise specified.


Serializer
----------
The serializer backend specifies how the data should be parsed from binary data to
python object.


Encryption
----------
A store's data-set is encrypted/decrypted by an encryption backend before sent
to the storage backend.


Storage
-------
A storage backend defines how the data for a store is stored and retrieved
(written/read). It does not concern itself with content but is a plain binary
reader/writer.
