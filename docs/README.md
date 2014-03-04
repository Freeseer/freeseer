[![Freeseer][freeseer-banner]][freeseer-docs]

Freeseer Documentation
----------------------

We use [Sphinx](http://sphinx.pocoo.org) to generate the project's documentation.
Documentation is written in [reStructuredText](http://docutils.sf.net/rst.html)
and stored in `.rst` files.

We use [Read the Docs](https://readthedocs.org/projects/freeseer/) for hosting.
RTD uses a [web hook](http://read-the-docs.readthedocs.org/en/latest/webhooks.html)
to build the documentation whenever we push to this repository.

Getting Started
---------------
The [Sphinx](http://sphinx.pocoo.org) website covers everything, but here's the
gist of what you need:

1. [Install Sphinx](http://sphinx-doc.org/latest/install.html): `pip install -U sphinx`
2. Use the [reStructuredText Primer](http://sphinx.pocoo.org/rest.html) as a reference when writing

Build & Preview your Changes Locally
------------------------------------

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

[freeseer-banner]: https://github.com/Freeseer/freeseer.github.io/raw/master/img/banner.png "Freeseer by FOSSLC"
[freeseer-docs]: http://freeseer.rtfd.org
