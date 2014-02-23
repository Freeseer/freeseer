Style Guide
===========

Every major project has its own style guide: a set of conventions (sometimes
arbitrary) about how to write code for that project. It's much easier to
understand a large codebase when all the code is in a consistent style.

Freeseer follows
`PEP 8 (Style Guide for Python Code) <http://www.python.org/dev/peps/pep-0008/>`_ and the
`Google Python Style Guide <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html>`_.
The two style guides mostly overlap but the Google one is more detailed and
easier to navigate. Freeseer also contains tests that will loosely check the code for PEP
8 compatibility.

Not all existing code follows these guidelines, but all new code is expected to.

Custom Guidelines
-----------------

There are a few exceptions or additions to the above style guides.

.. rubric:: Line Length

We use 120 characters at most, instead of the common 80-column limit.

.. rubric:: Python 3 Compatibility

Write code that's compatible with Python 3 whenever possible. This will make our
transition easier.

.. rubric:: Printing vs Logging

Do not print for debugging purposes, log instead. Make sure to `use the
appropriate logging level
<http://docs.python.org/2/howto/logging.html#when-to-use-logging>`_.
The logging calls may come in handy in the future, so consider leaving them in.

Use print when working on a CLI tool and the output must be shown to the end user.

.. rubric:: Log on a Per-Module Basis

Create an instance of a logger inside your module and name it after the module
that contains it by using ``__name__``.

Good::

  import logging
  log = logging.getLogger(__name__)
  log.info("All your base are belong to us")

Bad::

  import logging
  logging.info("For great justice")

.. rubric:: String Formatting

For logging, use printf style formatting.
For everything else, use ``str.format()``.

Good::

  log.info('%s : %d', key, value)
  greeting = 'Hello {} {}'.format(first_name, last_name)
  print('{0} - {1} - {0}'.format(foo, bar))

Bad::

  log.info(key + ' : ' + value)
  greeting = 'Hello %s %s' % (first_name, last_name)
  print foo, '-', bar, '-', foo

.. rubric:: Write Short Methods

Methods and functions should be kept small and focused.

Long methods are sometimes appropriate, so no hard limit is placed on method
length. However, if a method exceeds 40 lines or so, think about whether it can
be broken up without harming the structure of the program.

.. rubric:: Write Descriptive Docstrings

Comments should be descriptive ("Opens the file") rather than imperative ("Open
the file"). The comment *describes* the method, function, or class, it does not
tell it what to do.
