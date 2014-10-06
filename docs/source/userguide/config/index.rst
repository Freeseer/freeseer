Configuration (Settings)
========================

.. todo:: This page is still in progress.


General
-------


Command line
------------

There's currently two main configuration options:

.. glossary::

  ``freeseer config reset``
    Wipes various contents of the ``~/.freeseer`` directory.
    A fresh configuration is useful when encountering weird issues.

  ``freeseer config youtube``
    For configuring Freeseer's YouTube Uploader.
    The ``--client-secrets`` and ``--token`` options are used in the authentication process.

The ``-h/--help`` option can be used for more info.

.. code-block:: bash

  $ freeseer config --help
  usage: freeseer config [-h] {reset,youtube} ...

  positional arguments:
    {reset,youtube}
      reset          Reset Freeseer configuration and database
      youtube        Obtain OAuth2 token for Youtube access

  optional arguments:
    -h, --help       show this help message and exit

.. code-block:: bash

  $ freeseer config reset --help
  usage: freeseer config reset [-h] [-p PROFILE] {all,configuration,database}

  positional arguments:
    {all,configuration,database}
                          Resets Freeseer (default: all)

                                  Options:
                                      all           - Resets Freeseer (removes the Freeseer configuration directory, thus clearing logs, settings, and talks)
                                      configuration - Resets Freeseer configuration (removes freeseer.conf and plugins.conf)
                                      database      - Resets Freeseer database (removes presentations.db)


  optional arguments:
    -h, --help            show this help message and exit
    -p PROFILE, --profile PROFILE
                          Profile to reset (Default: default)

.. code-block:: bash

  $ freeseer config youtube --help
  usage: freeseer config youtube [-h] [--auth_host_name AUTH_HOST_NAME]
                                [--noauth_local_webserver]
                                [--auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]]
                                [--logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                                [-c CLIENT_SECRETS] [-t TOKEN]

  optional arguments:
    -h, --help            show this help message and exit
    --auth_host_name AUTH_HOST_NAME
                          Hostname when running a local web server.
    --noauth_local_webserver
                          Do not run a local web server.
    --auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]
                          Port web server should listen on.
    --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                          Set the logging level of detail.
    -c CLIENT_SECRETS, --client-secrets CLIENT_SECRETS
                          Path to client secrets file
    -t TOKEN, --token TOKEN
                          Location to save token file

Plugins
-------

See :doc:`plugins/index`.
