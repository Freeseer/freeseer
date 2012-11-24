Packaging guidlines for the currently supported operating systems and distributions
====================================================================================

Fedora/RedHat/CentOS/OpenSUSE Linux
------------------------------------

a) Build Freeseer using the instructions in the README.txt file
b) Create an RPM package by typing:

  python setup.py bdist_rpm --group="Sound and Video" --requires=python-feedparser,
  python-sqlite2,gstreamer,gstreamer-python,PyQt4

OR alternatively,

We have a handy "make rpm" target from the top level makefile that does both steps a and b
the "make rpm" target has a dependency on building the source
so this should happen automatically


Ubuntu/Debian Linux
-------------------

  Run "make deb" from the top level makefile

the "make deb" target has a dependency on building the source
so this should happen automatically


Arch Linux
----------


Instructions coming soon.


Windows
-------

In order to package for Windows, you require setuptools.
Be sure to install the right version for your version of python.

a) Build Freeseer using the instructions in the README.txt file
b) Create an RPM package by typing:

  python setup.py bdist_wininst


MacOS
-----

Sorry, we don't support MacOS just yet. We hope to soon.
