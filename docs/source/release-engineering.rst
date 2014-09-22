Release Engineering
===================

When releasing a new Freeseer version use the following checklist.

#. Ensure your git repo is clean
#. Update resource files
#.  * Navigate to src/freeseer/frontend/qtcommon and run "make"
#. ./bump_version.sh <new version>
#. git commit -a -s -m "Release 3.0.0"
#. git push origin master
#. Login to GitHub and navigate to a new release
#. Draft the release notes include new features and bugs fixed
#. Create python egg and source distribution:
#.  * python setup.py sdist
#.  * python setup.py bdist_egg
#. Push the source distribution to PyPi
#. Add the 2 binaries to the Release Draft
#. After peer review and release date agreed on Publish the release

.. note::
  The commit message summary line should say "Bump version to release
  version 3.0.0" (update version as relevant).

