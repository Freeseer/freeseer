Best Practices
==============

Don't Develop on Master Branch
------------------------------
The master branch is where code goes that's ready to ship.
It's way too risky to include development code on it.
Instead, base your development branch off Freeseer's experimental or development branch.


.. _branch-names:

Branch Names
------------
Try naming your development branch after the `issue <http://github.com/Freeseer/freeseer/issues>`_ you're working on.
Name it by issue # and description. For example, if you’re working on Issue #100, a new logo, your development branch should be called 100-new-logo.

.. seealso:: Want to `rename your branch <basics.html#renaming-your-branch>`_?

Multi-tasking
-------------
If you decide to work on another issue mid-stream, create a new branch for that issue—don’t work on multiple issues or features in one branch.
