Commandline
===========

The following commands are available:

* :ref:`Help`
* :ref:`Init`
* :ref:`Rm`
* :ref:`List`

For a full list of available commands and commandline options, run:

.. code-block:: console

    pycred --help

or for a specific command:

.. code-block:: console

    pycred COMMAND --help

To get more detailed logging, increase verbosity with one or more ``-v``.

.. code-block:: console

    pycred -v -v COMMAND


Help
----
The help command launches this extendend help, the user guide.

.. code-block:: console

    pycred help --pdf # PDF-version
    pycred help --html #HTML-version (default)


Init
----
The init command initializes/creates a new store.

.. code-block:: console

    pycred init NAME

The backends to use can be specified with commandline options. If a store with
the given name already exists, you will get an error. To re-initialize, delete
the store first (see :ref:`Rm`).


Rm
--
The rm command removes/deletes an existing store using its name.

.. code-block:: console

    pycred rm NAME


List
----
The list command lists all stores by name.

.. code-block:: console

    pycred list
