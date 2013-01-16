Installation
============

Here's everything you need to know to get Freeseer up and running.

.. note:: Freeseer stores its configuration settings in a `.freeseer` directory.
          On both Windows and Linux, the `.freeseer` directory is in the user's
          HOME directory. On Windows this is `C:\\Users\\username\\.freeseer\\`.
          On Linux it's `/home/username/.freeseer/`.

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

Visit our `download page <https://github.com/Freeseer/freeseer/downloads>`_
for installers for Debian/Ubuntu and Windows.

Build from Source
-----------------

Download the source code as a `zip <https://github.com/Freeseer/freeseer/zipball/master>`_ or
`tarball <https://github.com/Freeseer/freeseer/tarball/master>`_.

Alternatively, you can clone the project with git:

::

    $ git clone git@github.com:Freeseer/freeseer.git  # Clones a copy of the master repo

Potential contributors should :ref:`fork Freeseer <fork-freeseer-label>`.

.. todo:: Add build instructions (or just link to readme)

Installation of passlib for Freeseer Server          
*******************************************

Passlib needs to be installed to run the Freeseer Server.
It can be easily installed using this command:

::

    $ sudo easy_install passlib
