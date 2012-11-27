Test Suite
===================

.. rename all the next sub sections... they need to be more poignant

Setting up the Test environment
-------------------------------

Dependencies
************
* Checking you have all the dependencies


Extending the Test Suite
------------------------

Structure of /freeseer/test
***************************

* Best Practices

Adding/Editing a test module
****************************

* Writing a test module
** The example
** import unittest
** from freeseer.framework.presentation import Presentation
** class TestPresentation(unittest.TestCase):
** setUp, runTest, test_*, tearDown and the unittest "lifecycle"

* Python's unittest module "lifecycle"
** Case 1: User implements runTest()
** Case 2: User implements test_* methods
** The assert* family of methods

* Final thoughts
** Best practices

Running the Test Suite
-----------------------

* Introduction
* Unit test execution order
* Command line options
** Example #1: Discovery, Run all tests
** Example #2: Discovery, Verbose, Run all tests
** Example #3: Discovery, Verbose, Run until fail

Gotchas! a.k.a Q&A
-----------------------

* Question #1
* Question #2

