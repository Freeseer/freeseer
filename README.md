[![freeseer](https://github.com/Freeseer/freeseer.github.com/raw/master/img/banner.png
"Freeseer by FOSSLC")](http://freeseer.github.com)

Documentation
-------------

The Freeseer team uses a tool called [Sphinx](http://sphinx.pocoo.org) to create
the project's documentation.

Sphinx uses [reStructuredText](http://docutils.sf.net/rst.html) as its markup
language.

We chose Sphinx for several reasons:

* Easy to create intelligent and beatiful documentation
* Common tool for documenting projects written in Python
* Multiple output formats (HTML, LaTeX, manual pages, and plain text)
* Handles Python code, including highlighting, docstrings, and more

Getting Started
---------------
The best place to start is the [Sphinx](http://sphinx.pocoo.org) website.
But if you're in a hurry, here's the gist of what you need to know:

Install the Sphinx package with `sudo easy_install -U Sphinx`.

For an overview of basic tasks:

* [Sphinx tutorial](http://sphinx.pocoo.org/tutorial.html)

For a brief introduction on reStructuredText (reST) concepts and syntax:

* [reStructuredText Primer](http://sphinx.pocoo.org/rest.html)
* [Sphinx cheat sheet](http://matplotlib.sourceforge.net/sampledoc/cheatsheet.html)

Publishing to the Web
---------------------

Once you've made your changes to the documentation, you'll have to build the
output files with `make html`. By default the build directory is /build/.
We want the files in the HTML folder to go to the freeseer.github.com repo.

We can either put the output directly in the website repo, for example:

    $ sphinx-build -b html source path_to/freeseer.github.com/docs/
    # Better to do it this way than to modify the build path in make.bat,
    # since the path could vary by user.

or we can build to the default build path and run a script to copy the output
to the freeseer.github.com repo, commit, and push it for us:

    $ make html
    $ sh copy_commit_push.sh # Note: this script doesn't exist yet
