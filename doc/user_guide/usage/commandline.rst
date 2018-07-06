Commandline
===========

The following commands are available:

* :ref:`Help`
* :ref:`Init`
* :ref:`Set`
* :ref:`Get`
* :ref:`Unset`
* :ref:`Rm`
* :ref:`List`
* :ref:`Info`

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

    pycred help --pdf  # PDF-version
    pycred help --html  # HTML-version (default)


Init
----
The init command initializes/creates a new store.

.. code-block:: console

    pycred init STORE_NAME

The backends to use can be specified with commandline options. If a store with
the given name already exists, you will get an error. To re-initialize, delete
the store first (see :ref:`Rm`).


Set
---
The set command is used to input/set credentials for a user in a store.
By default the current system user is used.
The user and the username stored for the credential doesn't need to be the same.

The preferred way of providing the password is by entered it when prompted for it.
It can also be specified via the ``--password`` option, but it is much less secure since
it will show up in your console history and can be read from your screen.

An alternative user than the current user can be specified using the ``--user/-u`` option.

.. code-block:: console

    pycred set STORE_NAME USERNAME
    pycred set --user ALT_USER STORE_NAME USERNAME


Get
---
The get command is used to print the credentials for a user in a store.
By default the current system user is used.

An alternative user than the current user can be specified using the ``--user/-u`` option.

To specify what part of the credentials to print, use the ``--username/-n`` and ``--password/-p`` flags.

.. code-block:: console

    pycred get STORE_NAME --username -n -p
    pycred get --user ALT_USER STORE_NAME -p

If no print-flags are specified, nothing is printed. This mode can be used to
verify if a particular user exists in the store since the command will return exit code 0
if the user exists.

Unset
-----
The unset command is used to remove/unset credentials for a user in a store.
By default the current system user is used.

An alternative user than the current user can be specified using the ``--user/-u`` option.

.. code-block:: console

    pycred unset STORE_NAME
    pycred unset --user ALT_USER STORE_NAME


Rm
--
The rm command removes/deletes an existing store using its name.
Multiple names can be given in the same invocation.

.. code-block:: console

    pycred rm STORE_NAME...


List
----
The list command lists all stores by name.

.. code-block:: console

    pycred list

Info
----
The info command prints information about one or more stores. The output format
can be specified with the ``--format/-f`` option.

To print the users in the store, add the flag ``--users/-u``.

.. code-block:: console

    pycred info STORE_NAME...
    pycred info --users --format raw STORE_NAME
