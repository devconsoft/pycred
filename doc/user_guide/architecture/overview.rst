Architectural Overview
======================

.. uml:: overview.pu


Data-flow
---------
When an application uses pycred it requests the credentials using a credential-store
name and a username (that defaults to the current user).
The retrieved data-set contain a single username-password pair.

The store is configured to use a specific serializer, storage and encryption backends.
When a store is loaded, pycred reads the data from storage, using the stores
storage configuration. The read data is passed for decryption to the
encryption backend, before deserialized by the serializer-backend and returned in the form
of a credentials object.

.. uml:: dataflow.pu
