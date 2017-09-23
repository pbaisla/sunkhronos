sunkhronos
==========
Keep two folders on different devices in sync.

Usage
---------------
Sunkhronos can be run with the ``sunkhronos`` command. This command comes with two sub-commands called ``sunkhronos serve`` and ``sunkhronos connect``.

``sunkhronos serve`` is used to start a server that another device can connect to, to sync files:

.. code-block:: bash

    sunkhronos serve --port 8123 --directory . --backup-directory ./.sunkhronos-backup


``sunkhronos connect`` is used to connect to a server, to sync files:

.. code-block:: bash

    sunkhronos connect --host 172.31.85.100 --port 8123 --directory . --backup-directory ./.sunkhronos-backup

Please see the help information for these commands by typing:

.. code-block:: bash

    sunkhronos [command] --help


Installation
------------
Installing from PyPI using ``pip``:

.. code-block:: bash

    $ pip install sunkhronos

Installing from PyPI using ``easy_install``:

.. code-block:: bash

    $ easy_install sunkhronos

Installing from source:

.. code-block:: bash

    $ python setup.py install


Dependencies
------------
1. Python 3
2. ``twisted``
3. ``watchdog``
