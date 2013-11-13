Code Review
===========

We use `Pull Requests <https://help.github.com/articles/using-pull-requests>`_
on GitHub for code reviews and merging proposed changes.

Pull requests let you tell others about changes you've pushed to a GitHub
repository. Once a pull request is sent, we can review the set of changes,
discuss potential modifications, and you can even push follow-up commits if
necessary (without having to close and re-open the pull request).

.. seealso::

  - `Creating a pull request <https://help.github.com/articles/creating-a-pull-request>`_
  - `Merging a pull request <https://help.github.com/articles/merging-a-pull-request>`_
    (for anyone with push access to the destination repository)
  - `Closing a pull request <https://help.github.com/articles/closing-a-pull-request>`_

What we look for
################

in a pull request
^^^^^^^^^^^^^^^^^

- Descriptive title
- Summary describing the changes
- Points to and from the correct branches

  - From your development branch to Freeseer's master branch
- Reference any related issues or resources

in the code
^^^^^^^^^^^

- Code should follow our :doc:`coding-guidelines`
- Code is well documented

  - Documentation should also exist in our online documentation for any new features
- Logic of the code makes sense
- Code is efficient and readable
- Code is modular

  - Similar code should be put in functions
  - Functions should be small and focus on one thing
- Your code is thoroughly documented and uses
  `docstrings <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html?showone=Comments#Comments>`_ where appropriate
- Your branch can be merged cleanly into master

  - No merge conflicts
  - Your branch includes the latest commits from master (rebase to avoid merge commits)
- Includes unit tests for the new code
- All unit tests pass

in the commits
^^^^^^^^^^^^^^

- Each commit should represent one type of change
- Commit messages are as descriptive as possible
- Commit messages follow our `formatting guidelines
  <../best-practices.html#properly-style-your-commit-messages>`_
- `Squash related commits into a single commit
  <http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html>`_

Tips
####

- **Open a Pull Request as early as possible**

  Pull requests are a great way to start a conversation of a feature or a work
  in progress, so send one as soon as possible—even before you are finished with
  the code. Your team can comment on the feature as it evolves, instead of
  providing all their feedback at the very end.

- **Pull Requests work branch to branch**

  If you have push access to Freeseer/freeseer, you don't need to fork it to work on a new feature.
  Create your topic branch on Freeseer/freeseer instead, then make a pull request in the same repository.

- **A Pull Request doesn't have to be merged**

  Pull requests are easy to make and a great way to get feedback and track progress on a branch.
  But some ideas don't make it. It's *okay* to close a pull request without merging.

- **Anyone can review code**

  Reviewing code isn't exclusive to active contributors. Anyone is welcome and
  encouraged to review code—the more the better!
