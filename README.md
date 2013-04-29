[![freeseer](https://github.com/Freeseer/freeseer.github.io/raw/master/img/banner.png
"Freeseer by FOSSLC")](http://freeseer.github.com)
[![Build Status](https://travis-ci.org/Freeseer/freeseer.png)](https://travis-ci.org/Freeseer/freeseer-docs)

Freeseer's Documentation
------------------------

The Freeseer team uses a tool called [Sphinx](http://sphinx.pocoo.org) to create
the project's documentation.

Sphinx uses [reStructuredText](http://docutils.sf.net/rst.html) as its markup
language.

We chose Sphinx for several reasons:

* Easy to create intelligent and beatiful documentation
* Common tool for documenting projects written in Python
* Multiple output formats (HTML, LaTeX, manual pages, and plain text)
* Handles Python code, including highlighting, docstrings, and more
* Easy to track with git
  * Plus all the benefits of GitHub like pull requests, issue management, and a code review system

Getting Started
---------------
The best place to start is the [Sphinx](http://sphinx.pocoo.org) website.
But if you're in a hurry, here's the gist of what you need to know:

Install the Sphinx package with `sudo easy_install -U Sphinx`.

For an overview of basic tasks:

* [Sphinx tutorial](http://sphinx.pocoo.org/tutorial.html)

For a brief introduction on reStructuredText concepts and syntax:

* [reStructuredText Primer](http://sphinx.pocoo.org/rest.html)
* [Sphinx cheat](http://matplotlib.sourceforge.net/sampledoc/cheatsheet.html)
  [sheet](http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html)


Preview your Changes
--------------------

Note: You need to install Sphinx to preview your changes.

Once you've made your changes to the documentation, you need to rebuild the HTML
files using `make html`.

    cd freeseer-docs/
    make html

Your updated HTML files should be in`freeseer-docs/build/html/`.  
Open the relevant HTML file(s) with your favourite web browser!

**Tip:** GitHub can render reStructredText. View an `.rst` file to see how it looks.

**Tip:** View the underlying reStructuredText of any webpage built with Sphinx
by clicking the "Show Source" link on the page you're on.


Publish to the Web
-------------------

Once your changes are complete and look fine, they are ready to be deployed to
the online documentation at http://freeseer.github.com/docs.

We want the files in `./build/html/` to go to the
[freeseer.github.com](https://github.com/Freeseer/freeseer.github.com) repo.

A [script is provided](https://github.com/Freeseer/freeseer-docs/blob/master/publish.sh)
to easily build and publish the documentation online:

    $ ./publish

To add your own one-liner commit message, add it as an argument:

    $ ./publish 'Fix a typo.'

Or for a more manual approach, you can place the output directly in your local freeseer.github.com repo:

    $ sphinx-build -b html source path/to/freeseer.github.com/docs/
    # Don't forget to commit and push the changes in freeseer.github.com!

**Note:** This script is only intended for people with **write access** to the
[freeseer.github.com repo](http://github.com/freeseer/freeseer.github.com). It
builds the Sphinx output, copies the newly produced HTML files to your local
freeseer.github.com repo, then pushes them to GitHub.
