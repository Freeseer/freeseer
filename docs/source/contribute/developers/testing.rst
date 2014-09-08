Testing
=======

.. TODO: add short intro about automated testing
.. TODO: improve names of subsections
.. TODO: finish reviewing this page
.. TODO: reference Qt class docs (see Lance's last blog post) in See Also box

Configure your Test Environment
*******************************

If you can run Freeseer, you should have nothing to configure. This is because
Python's `unittest` module and PyQt's `QtTest` module are used for
Freeseer's test suite. The `unittest` module is Python's standard unit testing
framework, and thus part of the standard library. The `QtTest` module is
included with the PyQt4 package, which you should have installed as it's
a dependency for Freeseer.

If you want to make sure, you can start the Python interpreter and
import ``unittest`` and ``QtTest``::

  >>> import unittest
  >>> from PyQt4 import QtTest

If there are any errors, you won't be able to proceed with testing.


Extending the Test Suite
************************

Structure of Test Directory
---------------------------

As of Python 2.7, `unittest` supports (recursive) test module discovery.
All test modules should exist somewhere inside ``src/freeseer/tests/`` so that the
test suite can find them.

Since Freeseer is well organized into modules, we'd like to mirror this setup in the test folder. This means that if your code is located in src/freeseer/framework/core.py then your test code should be found in src/test/framework/test_core.py (more about file naming conventions later). We do this for logical ordering: it tells us that test modules in src/freeseer/test/folder_name are for testing modules in src/freeseer/folder_name.

If you are creating a new folder in src/freeseer/test/\*, ensure that your folder contains a __init__.py such that your test module can be imported by unittest during discovery.


Adding/Editing a test module
----------------------------

An example
^^^^^^^^^^

We now know where the test suite is located: src/freeseer/test.
We also know that the directory hierarchy below test matches the one below src/freeseer.
Next, as developers we'd like to add a new test module or modify an existing one.

Let's write a simple test case for the Presentation class found in src/freeseer/framework/presentation.py.
This class is simple, it is a model which holds data.
We pass a bunch of parameters and all the class attributes are public.
We'll create an instance, ensure the values we pass are correctly set and learn about the unittest module in the process.

We'll need to go to src/freeseer/test and check if there is a folder named framework.
If there isn't let's create it and immediately add an empty __init__.py inside it (see Note from part 2).

Next, we'll create our test module.
It would be nice to keep convention and name it test_presentation.py (i.e. the convention is test_my_module_name.py where the module counterpart is name my_module_name.py) but there is no way to enforce it.
As such this is going to be a "best practice".
Fortunately, unittest does enforce something: the name of the test module must have the form test_*.py or it will not be discovered.
Thus, your module name must start with **test_** and finish with **.py**.
This little bit can be configured (we'll see how in part 4), but the default pattern for unittest discovery is 'test_*.py'.

We now have our test module which can be found at: **src/freeseer/test/framework/test_presentation.py**.

Let's add some functionality!

**Note: The example used in the rest of this entry is to experiment with unittest and may not implement logical test cases!**

.. code-block:: python

  import unittest

  from freeseer.framework.presentation import Presentation

  class TestPresentation(unittest.TestCase):

    def setUp(self):
        self.pres = Presentation("John Doe", event="haha", time="NOW")

    def test_correct_time_set(self):
        self.assertTrue(self.pres.time == "NOW")
        self.pres.speaker = "John Doe"

    def test_speaker_not_first_param(self):
        self.assertNotEquals(self.pres.speaker, "John Doe")

    def test_event_is_default(self):
        self.assertFalse(self.pres.event != "Default")



There we have it, our first unit test to test Freeseer functionality!
Since there are no comments, let's go through it quick and take some time to understand the important parts:

import unittest
^^^^^^^^^^^^^^^

This will be in **every** test module. As we will see, each test class we write will subclass unittest.TestCase and this class is also where we get the assert* family of calls.


from freeseer.framework.presentation import Presentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will also be in **every** module but slightly modified.
Our target class to test this time is the Presentation class found in src/freeseer/framework/presentation.py.
When python loads the packages, it will convert src/freeseer/framework/presentation.py into freeseer.framework.presentation (this is an oversimplification of course).
Therefore, ensure your import path is correct for the target module. From the import path, simply import the class you wish to test against -- in our case this is Presentation.


class TestPresentation(unittest.TestCase):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**First: unittest.TestCase is required as the parent class or this will not be treated as a test class.**
This is the class we're creating which will encapsulate all the testing functionality for the Presentation class.
How do we know we're using this class to test the Presentation class? -- **we don't**.
It's up to the developer to name it appropriately and naming the class TestPresentation is another unenforceable best practice.


setUp, runTest, test_*, tearDown
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I invite you to read the `documentation <http://docs.python.org/2/library/unittest.html>`_.

The unittest.TestCase offers a "life cycle" a.k.a an ordered method call framework allowing a developer to setup, run and takedown tests respectively.

If the unittest.TestCase has implemented the setUp() method, then this method runs first. It is used to set-up any code required for the tests.

The next method which will run depends on whether the developer implemented runTest() or test_* methods.
The choice here is a matter of opinion, but if runTest() is implemented, then all tests are in this method.
If no assertion fails, runTest() will return OK, otherwise it will return **FAIL**.
If a collection of test_* methods are implemented, then we can still have several assertions in each test_* method, but now every individual test_* has an **OK/FAIL**.

If the unittest.TestCase has implemented the tearDown() method, then this method runs last. It is used to unset or destroy code required for the tests.


Python's unittest module "lifecycle"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a predefined order of execution for the above methods:

+ Case 1: User implements runTest()

  First, setUp() will be executed.

  If there is an exception, then then runTest() will not be executed. If setUp() succeeds, then runTest() is executed.

  Regardless of the result of runTest(), tearDown() will be executed.

+ Case 2: User implements test_* methods

  As above, if setUp() fails, then test_* will not be executed and regardless of the result of the test_* method, tearDown() will be executed.

  However, now for each test_* method, we will execute setUp(), a test_* method, then tearDown().

  *Note: The order in which test_\* methods are run is determined by their alphanumeric ordering. For a given unittest.TestCase class, the test_\* methods will sorted alphanumerically in increasing order, then run in this order. **

The assert* family of methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each of these has the power to **FAIL** a test_* or runTest method.
A test could contain several assert methods and will continue to run until an assertion fails.
If no assertion fails, then the test will be marked as OK.

A useful addition to the assert methods provided are the option to pass a message when the assertion fails. For example:

.. code-block:: python

  def runTest(self):
      self.assertEquals(3, 4, "Silly you, 3 is not 4!")

If the optional message ( "Silly you, 3 is not 4!" in this case) is given, then if the assertion fails the user will be given this optional message instead of the generic message.


Running the Test Suite
**********************

Introduction
------------

We've written our test case(s) and now we want to see the results. First, let's go over the expected results:

Recall: we are using the test_* methods, thus setUp() will execute before each test_* and the test_* methods will be executed in alphanumeric order. A test_* will FAIL if any of its assertions are false.

.. code-block:: python

  def setUp(self):
      self.pres = Presentation("John Doe", event="haha", time="NOW")

In setUp(), we are creating a Presentation instance and storing it in self.pres. Now, each test_* will access this instance using self.pres.

.. code-block:: python

  def test_correct_time_set(self):
      self.assertTrue(self.pres.time == "NOW")
      self.pres.speaker = "John Doe"

In test_correct_time_set(), we are checking that the time parameter in the constructor was correctly set to "NOW", then we are setting self.pres.speaker to "John Doe".

.. code-block:: python

  def test_speaker_not_first_param(self):
      self.assertNotEquals(self.pres.speaker, "John Doe")

In test_speaker_not_first_param(), we are checking that "John Doe" was in fact not set as the Presentation.speaker (it will be set as Presentation.title).

.. code-block:: python

  def test_event_is_default(self):
      self.assertFalse(self.pres.event != "Default")

Finally, in test_event_is_default(), we are checking that self.pres.event was set as "Default". Note that this case should fail.

Before we begin, a note about the alphanumeric order. The test_* methods will run in the following order:

  #. setUp(), test_correct_time()
  #. setUp(), test_event_is_default()
  #. setUp(), test_speaker_not_first_param()


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
what went wrong. Information related to which line the failure occured is
printed in the output's **FAILURES** section, as well as **DEBUG** or **INFO**
output that was printed to stderr in the erroneous code.
At the bottom of the output from the script statistics on code coverage are
displayed.

Gotchas! a.k.a Q&A
******************

**Q: Why didn't test_speaker_not_first_param() fail if it is being set to "John Doe" in test_correct_time_set() ?**

A: Because before test_speaker_not_first_param() is invoked, setUp() is executed which resets self.pres to a new instance. Thus self.pres is as it would be and self.pres.speaker = "".


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

