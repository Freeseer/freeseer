Basics
======

.. contents::
   :local:

Git & GitHub
------------

Freeseer is hosted on `GitHub <http://github.com>`_, which uses `Git
<http://git-scm.com/>`_. You'll generally encounter both while contributing.

Git allows many people to work on the same documents (e.g. source code) at the
same time, without stepping on each other's toes. It's a *distributed version
control system*. Git can be complicated for beginners or for people who have
previously used a version control system that's different by design (e.g. Subversion).

No worries, there are tons of online resources. If you can't find what you're
looking for, please ask us!

Before we begin, keep in mind that there is no *correct* way of using git. With
git, you can often achieve the same results via different ways. How you use git
is often determined by the guidelines of the project you're contributing to.
The examples on this page are how we recommend you use git when contributing to
Freeseer.

.. seealso::

   * Set up Git and your GitHub account
     → `help.github.com <http://help.github.com>`_

   * Learn by doing
     → `Try Git <http://try.github.com/>`_

   * Learn by watching
     → `Git Videos <http://git-scm.com/videos>`_

   * Learn by reading
     → `Pro Git book <http://book.git-scm.com>`_ (free)

   * Forgetful?
     → `Git Cheat Sheet <https://na1.salesforce.com/help/doc/en/salesforce_git_developer_cheatsheet.pdf>`_

   * Eclipse is your preferred IDE?
     → `Eclipse Git Plugin <https://github.com/blog/1181-eclipse-git-plugin-2-0-released>`_

   * Prefer GUIs over CLIs?
     → `GitHub for Windows <http://windows.github.com/>`_ or
     `GitHub for Mac <http://mac.github.com/>`_


.. _fork-freeseer:

Forking and Cloning Freeseer
----------------------------

1. Go to the `Freeseer repository <https://github.com/Freeseer/freeseer>`_ on
   GitHub and click the fork button. This creates your own public copy of the
   project under your GitHub profile (github.com/username/freeseer). A fork
   allows you to easily use someone's project as a starting point for your own.

.. image:: /images/fork.png
    :align: center
    :alt: Click the fork button on the page *github.com/Freeseer/freeseer*.

2. So far your fork only exists on GitHub. You'll need to clone it to your local
   machine to be able to work on the project. ::

    $ git clone https://github.com/your_username/freeseer.git

3. Your cloned repository has a default remote named ``origin`` that points to
   your fork on GitHub, which can be used for pushing and pulling updates.
   But there is no remote that points to the original repository that you forked
   from. Add a remote named ``upstream`` to keep track of the original Freeseer
   repository. ::

    $ cd freeseer
    $ git remote add upstream https://github.com/Freeseer/freeseer.git
    $ git remote -v # Lists your remotes, you should see origin and upstream

   .. tip:: The name ``upstream`` is by convention. You can use whatever name
     you prefer (e.g. ``mainstream`` or ``mothership``).


Basic Workflow
--------------

Whenever you're going to make a set of edits to the project, you should create a
topic branch (also called a feature branch) for your changes. Your topic branch
will usually be branched off of master.

Never make changes directly in the master branch. Your master branch should
mirror upstream's master branch, try to keep them in sync. You'll use
your local master branch to pull in changes from upstream.

1. Switch to the master branch and pull in the latest changes from upstream. ::

    $ git checkout master
    $ git pull upstream master

2. Create and checkout a new branch.
   Please follow our :ref:`naming guidelines <branch-names>`. ::

    $ git checkout -b my-topic-branch

3. Start making your changes. Commit early and often. ::

   $ git add modified_file
   $ git commit -m "Add foo" # Omit the -m flag to write a more detailed commit message.

4. After your first few commits, push your topic branch to GitHub. ::

   $ git push -u origin my-topic-branch # The next time you need to push, simply use git push

5. Go to GitHub and `open a pull request <https://help.github.com/articles/creating-a-pull-request>`_
   from your topic branch to upstream's master branch.

   This allows members of the `Freeseer organization <https://github.com/Freeseer?tab=members>`_
   to easily see updates made to your branch and perform code reviews as you
   make changes. So please **open a pull request as soon as possible!**

6. Rebase frequently to incorporate changes from upstream. ::

   $ git checkout master
   $ git pull upstream master
   $ git checkout my-topic-branch
   $ git rebase master

7. Push your commits to GitHub frequently. At a minimum, push your changes when
   you're done working for the day.

8. When you consider your work complete and ready to be merged, rebase any
   changes from upstream into your branch once more (see step 6).

9. `Squash <http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html>`_
   any dirty commits via an interactive rebase, so the remaining commits are
   meaningful and comprehensible. For example, squash commits that
   only fix a typo or whitespace, and rewrite poor commit messages. ::

   $ git rebase -i master

10. Let others know you consider your work ready to be merged by leaving a
    comment in your pull request. :doc:`You may be asked to make some changes.
    <developers/pull-requests-and-code-review>`

11. When your pull request has been merged, celebrate, then clean up by deleting
    your local and remote topic branch. ::

    $ git checkout master
    $ git pull
    $ git branch --delete my-topic-branch # Deletes the topic branch on your machine (can also use -d)
    $ git push --delete my-topic-branch # Deletes the topic branch on your fork

.. warning:: Performing an interactive rebase (as in step 9) will `rewrite
             history <http://git-scm.com/book/en/Git-Tools-Rewriting-History>`_,
             and should therefore only be used on personal branches.
             Never rewrite history on branches that others are also working on.

.. tip:: If you rewrite history that's already been pushed, you'll need to
         force push the next time (``git push -f``). Try to avoid forced pushes
         by only editing commits that haven't been pushed yet.
         Use ``git rebase -i HEAD~N`` to edit the last *N* commits.

Workflow Diagram
----------------
A visual representation of what a contributor's workflow should look like.

.. image:: https://docs.google.com/drawings/d/1hPslTdzT7SLZsudFGOIS9M5o6G1Q3HcY4-q0F8BNKWQ/pub?w=737&h=619
    :alt: Contributor's workflow diagram


Reference Issues in your Commit Messages
----------------------------------------

.. note::
  We use a single issue tracker for all of our repositories:
  `github.com/Freeseer/freeseer/issues <https://github.com/Freeseer/freeseer/issues>`_

Similar to how GitHub allows you to `reference issues and commits from a comment
on GitHub.com <https://github.com/blog/957-introducing-issue-mentions>`_, you
can also reference issues from a commit message.

.. tip::
  Referencing issues from your commit messages makes it easy to view more context
  and see which commits are related.

There are two ways to reference issues.

1. Short form: `#123` or `GH-123`
2. Long form: `user/repo#123`

You can reference issues that belong to different repositories on GitHub using
the long form. This is called a cross-repo reference.

If you forked a repository, you can use the short form to reference issues
belonging to the original repository.

To close an issue from a commit message [#issue-permissions]_, place a supported
keyword directly in front of the reference.
For example, "Close #123" or "Fix gh-123".

.. rubric:: Supported keywords
.. hlist::
   :columns: 3

   * close
   * closes
   * closed
   * fix
   * fixes
   * fixed
   * resolve
   * resolves
   * resolved

You can also close multiple issues in a single commit message, and close issues
cross-repo if you use the long form. [#close-issues-cross-repo]_

.. tip::
  GitHub is case-insensitive to commit messages.

.. seealso::
  `Closing issues via commit messages
  <https://help.github.com/articles/closing-issues-via-commit-messages>`_

Dealing with Conflicts
----------------------

You'll run into a merge conflict eventually.
It's when something doesn't match up between the local and remote copy of a file.
To be more precise, a merge conflict usually occurs when your current branch and the branch you want to merge into the current branch
have diverged. That is, you have commits in your current branch which are not in the other branch, and vice versa.

The secret is to use ``git mergetool``. Here's one way how you can resolve conflicts::

    $ git fetch upstream
    $ git rebase upstream/experimental current-local-branch
    ... CONFLICT: Merge conflict in <filenames>

Now you have 3 options:

1) Selectively choose which parts of a file to use (using an external visual diff & merge tool)::

    $ sudo apt-get install meld  # Install Meld (or at http://meld.sourceforge.net)
    $ git mergetool -t meld  # Some alternatives are kdiff3, opendiff, diffmerge, etc.
    ... The visual merge tool is launched.
    ... It shows three versions of the file (local, failed merge, remote).
    ... You can easily choose code from any and all of them to resolve conflicts.
    ... Don't forget to save the file when you're done.

2) Ignore their changes, use your file::

    $ git checkout --ours <filename>

3) Ignore your changes, use their file::

    $ git checkout --theirs <filename>

Once you've resolved all conflicts::

    $ git add <filename>  # Or 'git add .' to mark all files as resolved
    $ git rebase --continue

To abort the conflict merging process at any time::

    $ git rebase --abort


Renaming your Branch
--------------------

Want to use a better name for your branch?

Renaming a local branch::

    $ git branch --move old-name new-name  # Short option is -m

Renaming a remote branch is more difficult because git doesn't support it.
A workaround is to delete the branch and re-add it with the new name::

    $ git push origin new-name
    $ git push origin --delete old-name


Reporting Bugs & Requesting Features
------------------------------------

.. glossary::

  1. Search
      We troubleshoot and discuss features in public. If you've found a bug or have
      an idea, take a few minutes to see if it's already been documented.

      Search our :doc:`documentation </index>`, :ref:`mailing list <mailing-list>`,
      `issue tracker <https://github.com/Freeseer/freeseer/issues>`_, and
      `IRC log <https://botbot.me/freenode/freeseer/>`_.

  2. Ask
      Contact us before opening a new issue, otherwise you risk it being closed for
      reasons such as it being a known issue or previously rejected idea.

      Hop in our :ref:`IRC channel <irc>` or send an email to the
      :ref:`mailing list <mailing-list>` and describe your problem or idea.

  3. Open a new issue
      After searching and contacting us, `open an issue
      <https://github.com/Freeseer/freeseer/issues/new>`_ if none exist and
      reference any existing related issues that you know of.

      If you're a new contributor, please use one of the templates below.

Bug Report Template
*******************

For bug reports, describe step by step exactly what you did and what went wrong.

::

    Steps to reproduce the problem:
    1.
    2.
    3.


    What is the expected behavior?


    What went wrong? (Place any screenshots here)


    Did this work before?
    - Not applicable / I don't know
    - Yes, this is a regression
    - No, I think it never worked


    Any other comments? (E.g. Freeseer version, Python version, operating system, error messages, etc.)

Or use this conciser template::

    Steps:
    1.
    2.
    3.

    Expected:

    Observed:

    Notes:

Feature Request Template
************************

::

    Purpose of feature (pros, cons, use cases):


    Describe the feature and its functionality:


    Mockups / Screenshots / Examples:

Of course you can also argue feature removal.


.. rubric:: Footnotes

.. [#issue-permissions]
   You can only close an issue from a commit message if you have push access
   to that repository. In other words, if you can close the issue from
   GitHub.com, you can also close it from a commit message.

.. [#close-issues-cross-repo]
   This is useful when closing an issue in Freeseer/freeseer from a commit
   that belongs to another repository under the Freeseer organization.
