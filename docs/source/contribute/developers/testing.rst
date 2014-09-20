Testing
=======

.. TODO: add short intro about automated testing
.. TODO: improve names of subsections
.. TODO: finish reviewing this page
.. TODO: reference Qt class docs (see Lance's last blog post) in See Also box


Configure your Test Environment
*******************************

Freeseer should not need additional configuration after installing the
:ref:`development requirements<pypi-packages>`. This is because Python's ``pytest`` and PyQt's ``QtTest``
module are used for Freeseer's test suite. The ``pytest`` module is a feature
rich testing framework that makes writing tests simple. The ``QtTest`` module is
included with the PyQt4 package, which you should have installed as it's
a dependency for Freeseer.

If you want to make sure you have the packages, you can start the Python
interpreter and
import ``pytest`` and ``QtTest``::

  >>> import pytest
  >>> from PyQt4 import QtTest

If there are any errors, you won't be able to proceed with testing.


Extending the Test Suite
************************

Structure of Test Directory
---------------------------

All of Freeseer's tests exist in ``src/freeseer/tests/``.
Since Freeseer is well organized into modules, we'd like to mirror this setup
in the test folder. This means that if your code is located in
``src/freeseer/framework/core.py`` then your test code should be found in
``src/freeseer/tests/framework/test_core.py`` (more about file naming
conventions later). We do this for logical ordering: it tells us that test
modules in ``src/freeseer/tests/folder_name`` are for testing modules in
``src/freeseer/folder_name``.

If you are creating a new folder in ``src/freeseer/tests/``, ensure that your
folder contains a ``__init__.py`` such that your test module can be imported.


Adding/Editing a test module
----------------------------

An example
^^^^^^^^^^

We show a set of test methods for the database class found in
``src/freeseer/framework/database.py``.
This class contains a database connector that lets the framework fetch stored
data efficiently.
The purpose of this unit test is to demonstrate some of the functionality
that is provided by ``pytest``.

To create a test module make an empty file with the name
``test_database.py``.
The convention used by Freeseer is ``test_module_name.py`` where the module
counterpart is name ``module_name.py``.
Thus, your module name should start with **test_** and finish with **.py** at
the very least.

Let's add fake functionality to the test module ``test_database.py``!


.. code-block:: python

  import os

  from PyQt4 import QtSql
  import pytest

  from freeseer.framework.config.profile import Profile
  from freeseer.framework.plugin import PluginManager
  from freeseer.framework.presentation import Presentation

  @pytest.fixture
  def db(tmpdir):
      """Construct a database connector fixture"""
      profile_path = str(tmpdir)
      profile = Profile(profile_path, 'testing')
      return profile.get_database()

  def test_query_result_type_is_query(db):
      assert isinstance(db.get_talks(), QtSql.QSqlQuery)
      assert isinstance(db.get_events(), QtSql.QSqlQuery)
      assert isinstance(db.get_talk_ids(), QtSql.QSqlQuery)
      assert isinstance(db.get_talks_by_event('SC2011'), QtSql.QSqlQuery)
      assert isinstance(db.get_talks_by_room('T105'), QtSql.QSqlQuery)

  def test_query_result_type_is_presentation(db):
      assert isinstance(db.get_presentation(1), Presentation)

  def test_query_result_type_is_model(db):
      assert isinstance(db.get_presentations_model(), QtSql.QSqlTableModel)
      assert isinstance(db.get_events_model(), QtSql.QSqlQueryModel)
      assert isinstance(db.get_rooms_model('SC2011'), QtSql.QSqlQueryModel)
      assert isinstance(db.get_talks_model('SC2011', 'T105'), QtSql.QSqlQueryModel)

  def test_add_talks_from_csv(db):
      """Test that talks are retrieved from the CSV file"""

      dirname = os.path.dirname(__file__)
      fname = os.path.join(dirname, 'sample_talks.csv')

      presentation = Presentation('Building NetBSD', 'David Maxwell')

      db.add_talks_from_csv(fname)
      assert(db.presentation_exists(presentation))


Break down of the unit test:

import pytest
^^^^^^^^^^^^^

This lets us use all of the testing features provided by ``pytest`` like
fixtures and function tests. It should be noted, unit tests written using the
old framework will import the ``unittest`` module instead.


@pytest.fixture
^^^^^^^^^^^^^^^

pytest provides fixture objects which allows a developer to put frequently
created function call results into an object.
Fixtures can be used in
place of conventional setup functions as in ``unittest``. In the
example, the fixture contains a QtDBConnector object which all of the test
methods can access. ``unittest`` teardown functions can be written with
yield fixtures. Documentation on
`fixtures <http://pytest.org/latest/fixture.html>`_ is available from pytest.


pytest test_* functions
^^^^^^^^^^^^^^^^^^^^^^^

``pytest`` will recurse into directories (that are not marked as
*norecursedirs*), will look for ``test_*.py`` or ``*_test.py`` files, ``Test``
prefixed test classes, and ``test_`` prefixed functions.
``pytest`` will also discover traditional ``unittest.TestCase`` tests.
Further documentation
can be found on the `pytest <http://pytest.org/latest/goodpractises.html#conventions-for-python-test-discovery>`_ site.

It should be noted that testing the return type of function calls in unit
tests is not very useful, as in the example ``test_query_result_type_*()``.

The assert methods
^^^^^^^^^^^^^^^^^^

Each ``assert`` has the power to **FAIL** a ``test_*`` method.
A test could contain several assert methods and will continue to run until an assertion fails.
If no assertion fails, then the test will be marked as OK.
It is important not to write too many assert statements in a test method. If
this occurs than the test is probably trying to cover too many test scenarios
and therefore the test should be broken up into smaller parts.

If an assertion fails ``pytest`` will give very generous failure information. For example, with the use of a fake test file:

.. code-block:: python

   import pytest

   def test_crustacean():
       assert 'lobster' == 'crab'


The fake script will fail because the two strings are not equivalent, it will
output the following when ``$ py.test test_crustacean.py`` is run from the
command line:

.. code-block:: none

  ============================= test session starts ==============================
  platform linux2 -- Python 2.7.6 -- py-1.4.23 -- pytest-2.5.2
  plugins: cov
  collected 1 items 

  test_crustacean.py F

  =================================== FAILURES ===================================
  _______________________________ test_crustacean ________________________________

      def test_crustacean():
  >       assert 'lobster' == 'crab'
  E       assert 'lobster' == 'crab'
  E         - lobster
  E         + crab

  test_crustacean.py:6: AssertionError
  =========================== 1 failed in 0.01 seconds ===========================


Running the Test Suite
**********************

Introduction
------------

We've written our test case(s) and now we want to see the results. First, let's go over the expected results:

.. code-block:: python

  @pytest.fixture
  def db(tmpdir):
      """Construct a database connector fixture"""
      profile_path = str(tmpdir)
      profile = Profile(profile_path, 'testing')
      return profile.get_database()

The ``pytest`` fixture creates an instance of the QtDBConnector object and
allows each method matching the ``test_*`` pattern to have access to it.
The fixture is created each time a ``test_*`` function receives it as an
argument. The argument ``tmpdir`` is a ``pytest`` built in test function
argument that provides a unique temporary directory to each test function
that calls it.
The example recreates the ``QtDBConnector`` each time a
test function uses the ``db`` fixture. If you need to finer control over
how the fixture is created then refer to the pytest documentation.

.. code-block:: python

  def test_query_result_type_is_query(db):
      assert isinstance(db.get_talks(), QtSql.QSqlQuery)
      assert isinstance(db.get_events(), QtSql.QSqlQuery)
      assert isinstance(db.get_talk_ids(), QtSql.QSqlQuery)
      assert isinstance(db.get_talks_by_event('SC2011'), QtSql.QSqlQuery)
      assert isinstance(db.get_talks_by_room('T105'), QtSql.QSqlQuery)

  def test_query_result_type_is_presentation(db):
      assert isinstance(db.get_presentation(1), Presentation)

  def test_query_result_type_is_model(db):
      assert isinstance(db.get_presentations_model(), QtSql.QSqlTableModel)
      assert isinstance(db.get_events_model(), QtSql.QSqlQueryModel)
      assert isinstance(db.get_rooms_model('SC2011'), QtSql.QSqlQueryModel)
      assert isinstance(db.get_talks_model('SC2011', 'T105'), QtSql.QSqlQueryModel)


In the ``test_query_result_type_is_*()`` test functions, we are checking that
the database queries return expected types.


.. code-block:: python

  def test_add_talks_from_csv(db):
      """Test that talks are retrieved from the CSV file"""

      dirname = os.path.dirname(__file__)
      fname = os.path.join(dirname, 'sample_talks.csv')

      presentation = Presentation('Building NetBSD', 'David Maxwell')

      db.add_talks_from_csv(fname)
      assert(db.presentation_exists(presentation))

Finally, in ``test_add_talks_from_csv()``, we are checking that we can also
add talks from comma separated value format files.


Command line options
--------------------

**Note: to avoid package import errors, we need to run the following commands from the src folder.**

Example: Run all tests with pytest
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run all of the tests in ``src/freeseer/tests/``, issue the following command from
the ``src/`` directory:

.. code-block:: none

   $ python setup.py test

The output will contain information about the test session. If there are any
failures during the session then failure messages will be logged and testing
will continue.
If there is a failure, the developer may read through the output to see
what went wrong. Information related to which line the failure occurred is
printed in the output's **FAILURES** section, as well as **DEBUG** or **INFO**
output that was printed to stderr in the erroneous code.
At the bottom of the output from the script statistics on code coverage are
displayed.

Gotchas! a.k.a Q&A
*******************

**Q: I set a variable in one of my unit tests, but my other unit tests cannot
see the values I set!**

A: There is no guarantee for the order in which unit tests run. It is also not
a good practice to have dependencies between unit tests. Each of the unit tests
should be stand alone and should not alter the test environment for tests
running after said unit test. If you want to test that a unit test produces
a given value, then the result of the unit test could be compared to a fixture
to assert the condition has been met. The same fixture could then be used in
the following unit test that you were using the result of the prior unit test
in. This would separate the two unit tests from depending on the order in which
they are ran by the test suite.

**Q: Can pytest run UnitTest files?**

A: Yes, ``pytest`` can run ``unittest.TestCase`` based unit tests if they follow the
test discovery naming conventions.

What should testers focus on?
-----------------------------

Ultimately, testers should protect users and the organization from bad design,
confusing UX, functional bugs, security and privacy issues, and so forth.

Some things testers should consider:

· Where are the weak points in the software?

· What are the security, privacy, performance and reliability concerns?

· Do all the primary user scenarios work as expected? For all international audiences?

· Does the product interoperate with other products (hardware and software)?

· In the event of a problem, how good are the diagnostics?

