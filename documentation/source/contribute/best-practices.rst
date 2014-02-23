Best Practices
==============

Don't Develop on Master Branch
------------------------------

The master branch contains stable code that's ready to ship. The master branch
build should always be passing.

The maintenance branch (if it exists) contains patches for the latest release,
and doesn't get any new features.

Use topic branches instead of working directly on master.

.. _branch-names:

Name Your Branch After an Issue or Task
---------------------------------------

If an `issue exists <http://github.com/Freeseer/freeseer/issues>`_ for the task
you're going to work on, name your new branch after the issue # and description.
For example, if you're working on Issue #100, a new logo, your branch name would
be "100-new-logo".

If you'll be working on a task which no issue exists for, consider creating an
issue for it. If you decide to go issue-less, at least give your branch a
descriptive name that matches the task you'll be working on.

.. seealso:: Could your branch name be improved?
             `Rename your branch! <basics.html#renaming-your-branch>`_

Start a New Task on a New Branch
--------------------------------

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

Properly Style Your Commit Messages
-----------------------------------

To help keep the style of our commit messages consistent and for easier viewing
on GitHub, please write your commit messages in accordance with this style::
    
    Capitalized and concise (50 chars or less) summary of your commit

    More detailed explanatory text if necessary. Wrap at 72 characters.
    Notice that the above summary message does not end with a period,
    and there's a blank line between the summary and body text.

    If the commit fixes an issue, start the summary line with "Fix",
    followed by the issue number. E.g. "Fix #123 Add foo to bar".

    - Bullet points (hyphens or asterisks) are allowed

    - No ending period needed and wrap at 72 chars

    - Put a space after bullet points and blank lines between them

    - Use imperative, present tense: "fix", not "fixed" or "fixes"

    - Add any references to related issues on GitHub if possible

    Last paragraph should reference related issues and pull requests.
    Fix #123
    Close #321
    Related to #404

If you can describe your commit with just a summary line, you may use
git commit's message argument::

    git commit -m "Summary of your commit (50 chars or less)"
