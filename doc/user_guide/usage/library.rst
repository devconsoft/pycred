Library
=======

All the examples assumes the following imports:

.. code-block:: python

    from pycred.pycred import PyCred

The main library is implemented in the :ref:`Class PyCred`.


Initialize a New Store
----------------------
The below example illustrates how a store is initialize and saved, named *mystore*
with default serializer, clear encryption and file storage.

.. code-block:: python

    pc = PyCred()
    store = pc.init_store('mystore', encryption='clear', storage='file')


Set, Get and Unset Credentials
------------------------------
The basic operations of setting, getting and unsetting credentials in a store can
be done either via a :ref:`Class Store` object, or via an instance of the main library :ref:`Class PyCred`.
Interacting with PyCred acts on a higher level of abstraction, while the Store requires
more details.

The best way to illustrate the differences is via examples. Both the Store and PyCred
examples performs the standard operations of setting (saving) credentials, getting (retrieving)
saved credentials and unsetting (removing) credentials for a user.

The below example assumes that a *store* has been initialized as in :ref:`Initialize a New Store`,
or retrieved from PyCred via ``store = PyCred().get_store('mystore')``.

.. code-block:: python

    from pycred.credentials import Credentials

    user = 'user'
    cred = Credentials('username', 'password')
    store.set_credentials(user, cred)
    cred = store.get_credentials(user)
    store.unset_credentials(user)


The below examples assumes that a store exists with the name *mystore*.
In this example are we using the default user instead of providing one.

Using the library is some-what less efficient because the store object is recreated
from configuration on the file-system between each call.

.. code-block:: python

    pc = PyCred()
    store = 'mystore'
    pc.set_credentials(store, 'username', 'password')
    cred = pc.get_credentials(store)
    pc.unset_credentials(store)


Class PyCred
------------
.. autoclass:: pycred.pycred.PyCred
   :members:


Class Store
-----------
.. autoclass:: pycred.store.Store
   :members:


Class Credentials
-----------------
.. autoclass:: pycred.credentials.Credentials
   :members:
