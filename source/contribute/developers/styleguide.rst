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

Custom Guidelines
-----------------

There are a few exceptions or additions to the above style guides.

.. rubric:: Line Length

We use 120 characters at most, instead of the common 80-column limit.

.. rubric:: Python 3 Compatibility

Write code that's compatible with Python 3 whenever possible. This will make our
transition easier.

.. rubric:: Printing vs Logging

You should never print to debug, log instead. Chances are the logging will
come in handy in the future so you may as well leave it in.

Use print when working on a CLI tool and the output must always be shown to the
end user.

.. rubric:: String Formatting

For logging, use ``logging.info("%s %s", foo, bar)`` (with the appropriate
logging level of course).

For everything else, use ``str.format()``. E.g. ``'{} - {}'.format(foo, bar)``
or ``'{0}, {1}, {0}'.format(foo, bar)``.
