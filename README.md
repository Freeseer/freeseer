[![freeseer](https://github.com/Freeseer/freeseer.github.io/raw/master/img/banner.png
"Freeseer by FOSSLC")](http://freeseer.github.com)
[![Build Status](https://travis-ci.org/Freeseer/freeseer.png)](https://travis-ci.org/Freeseer/freeseer-docs)

Freeseer Documentation
----------------------

We use [Sphinx](http://sphinx.pocoo.org) to generate the project's documentation.
Documentation is written in [reStructuredText](http://docutils.sf.net/rst.html)
and stored in .rst files.

We chose Sphinx for several reasons:

* Easy to create intelligent and beatiful documentation
* Common tool for documenting projects written in Python
* Multiple output formats (HTML, LaTeX, manual pages, and plain text)
* Handles Python code, including highlighting, docstrings, and more
* Easy to track with git
  * Plus all the benefits of GitHub like pull requests, issue management, and a code review system

Getting Started
---------------
The [Sphinx](http://sphinx.pocoo.org) website covers everything, but here's the
gist of what you need:

1. [Install Sphinx](http://sphinx-doc.org/latest/install.html): `pip install -U sphinx`
2. Use the [reStructuredText Primer](http://sphinx.pocoo.org/rest.html) as a reference when writing

Build & Preview your Changes
----------------------------

**Note:** You need to have the [freeseer repository](https://github.com/freeseer/freeseer)
          checked out at the same top level directory as the freeseer-docs repository.
          This allows the Freeseer source code to be discoverable when
          generating documentation from docstrings. Note that these docstrings
          must be written in reStructuredText format and Sphinx markup can be used.

Once you've made your changes to the documentation, rebuild the HTML output.

    $ cd freeseer-docs/
    $ make html

Your updated HTML files should be in`freeseer-docs/build/html/`,
and you can view them with your web browser.

**Tip:** GitHub can render reStructredText (but doesn't support Sphinx markup).
         View any .rst file to see how it looks.

**Tip:** View the underlying reStructuredText of any webpage built with Sphinx
         by clicking the "Show Source" link on the page you're on.

Publish to the Web
-------------------

Once your changes are complete and look fine, they are ready to be deployed to
the online documentation at http://freeseer.github.io.

We want the files in `./build/html/` to go to the
[freeseer.github.io](https://github.com/Freeseer/freeseer.github.io) repo.

A [script is provided](https://github.com/Freeseer/freeseer-docs/blob/master/publish.sh)
to easily build and publish the documentation online:

    $ ./publish

To add your own one-liner commit message, add it as an argument:

    $ ./publish 'Fix a typo.'

Or for a more manual approach, you can place the output directly in your local freeseer.github.com repo:

    $ sphinx-build -b html source path/to/freeseer.github.io/
    # Don't forget to commit and push the changes in freeseer.github.io!

**Note:** This script is only intended for people with **write access** to the
[freeseer.github.io repo](http://github.com/freeseer/freeseer.github.io). It
builds the Sphinx output, copies the newly produced HTML files to your local
freeseer.github.com repo, then pushes them to GitHub.
