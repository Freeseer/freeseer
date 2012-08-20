Installation
============

Here's everything you need to know to get Freeseer up and running.

Prerequisites
-------------
* Python 2.7
* Sqlite3
* PyQt4
* python-feedparser
* python-setuptools
* yapsy (needs setuptools to install)
* passlib (this is required for the server)

Installers
----------

Visit our `download page <https://github.com/Freeseer/freeseer/downloads>`_ for installers for Debian/Ubuntu and Windows.

Build from Source
-----------------

Download the source code as a `zip <https://github.com/Freeseer/freeseer/zipball/master>`_ or
`tarball <https://github.com/Freeseer/freeseer/tarball/master>`_.

Alternatively, potential contributors can clone the project with git:

::

    $ git clone git@github.com:Freeseer/freeseer.git  # Clones a copy of the master repo

.. todo:: Add build instructions (or just link to readme)

OS-Specific Plugins
-------------------

Plugins offer extra functionaltiy, so you'll want to download them.

We have OS-specific repositories to simplify the organization of Freeseer plugins.

Clone the OS-specific plugins to your `~/.freeseer/plugins` directory
and Freeseer should detect them.

`Linux Plugins <https://github.com/Freeseer/freeseer-plugins-linux>`_
**************

::

    $ git clone git@github.com:Freeseer/freeseer-plugins-linux.git ~/.freeseer/plugins


`Windows Plugins <https://github.com/Freeseer/freeseer-plugins-windows>`_
****************

::

    $ git clone git@github.com:Freeseer/freeseer-plugins-windows.git ~/.freeseer/plugins

.. note:: On both platforms the `.freeseer` directory is in the user's HOME
          folder. On Windows this is `C:\\Users\\username\\.freeseer\\`.

Installation of passlib for Freeseer Server          
*******************************************

Passlib needs to be installed to run the Freeseer Server.
It can be easily installed using this command:

::

    $ sudo easy_install passlib