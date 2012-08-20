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

Starting a New Task
-------------------

Using git requires a certain mindset:

* **Branches** are **tasks**
* **Commits** are **subtasks**

Tasks are major changes to the codebase, such as a new feature.
Tasks are usually projects of their own and require a large amount of work.
A task can be broken down into subtasks. These are the smaller problems that
need to be solved to make progress towards your larger task.

Each new task should have its own branch. Why?

- Your work is more organized (separate branches for separate tasks)
- Easier for everyone to see what task you're working on
- Reduces the risk of introducing new bugs
- Easier to isolate and fix new bugs
- Good for experimenting as nothing outside that branch is harmed
