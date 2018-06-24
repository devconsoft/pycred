Introduction to PyCred
======================

PyCred is a debian and python package for handling user credentials.

It can be used by humans as a stand-alone application, and by application
developers as a python library.

See also :ref:`PyCred Usage`.


High Level Concepts
-------------------
Credentials are stored in *stores*. *Backends* for the tasks of *serialization*,
*encryption* and *storage*, determine how a particular store operates.

The store is accessed as a *user* (usually the executing system user), to retrieve
or store the credentials of that user.

For a more technical oriented description, see :ref:`Architectural Overview`.

See also :ref:`Configuration`.


Stores
------
PyCred groups its data into stores. A store uses a specified
serializer backend, storage backend and encryption backend.

When using the pycred library, an application will request
the credentials for a particular store as a particular user.

A store only holds one username-password pair per user.
This to ensure the credentials are unambiguous for the given context.

Even if a user only is allowed a single set of credentials in a store,
it allows for multiple users storing their credential in the same store.
This to allow for central stores in multi-user contexts.

The system username might be different than the username in the credentials.

When creating a new store, the default serializer, storage and encryption backends
will be used unless otherwise specified.


Credentials
-----------
Credentials are a value pair consisting of *username* and *password*.

Backends
--------
*Backend* is a common name for:

* :ref:`Serializers`
* :ref:`Encryptions`
* :ref:`Storages`

Serializers
~~~~~~~~~~~
The selected serializer determine how the credentials is serialized from python
object to *data* in a store.

Encryptions
~~~~~~~~~~~
The selected encryption determine how serialized data is encrypted in a store.

Storages
~~~~~~~~
The selected storage determine how the encrypted data is persisted/stored.
