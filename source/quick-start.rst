Quick-Start Guide
=================

Freeseer is a free and open source screencasting application, primarily
developed for capturing and streaming computer-aided presentations at conferences.

It's been successfully used to capture presentations, demos, training material,
and other videos. It's capable of handling large conferences with many talks
in various rooms.

With Freeseer, you can record video from external sources such as FireWire and
USB (e.g. webcam or another computer's screen via VGA output [#f1]_).

Freeseer is written in Python, uses Qt4 for its GUI, and Gstreamer for video/audio processing.
And it's based on open standards so it supports royalty free audio and video codecs.

`Read our history <http://fosslc.org/drupal/node/596>`_ to find out why Freeseer
was created.


Installing Freeseer from a package
-----------------------------------
Use this option if you just want to run Freeseer. If you plan on developing
Freeseer, skip to the next section: :ref:`install-for-dev`.

Arch Linux
**********
Freeseer is available in AUR: https://aur.archlinux.org/packages/freeseer-git/

Or install with yaourt::

    yaourt -S freeseer-git

Gentoo Linux
************
Freeseer is available in PaddyMac's portage overlay: https://github.com/PaddyMac/overlay

After adding this overlay::

    emerge -av freeseer

OpenSUSE
********
Freeseer is available in the OpenSUSE repository::

    zypper install freeseer


Python Package Index
********************
Freeseer can also be installed with pip::

    pip install freeseer


.. _install-for-dev:

Installing Freeseer for Development
-----------------------------------

Dependencies
************
+ Git
+ Python 2.7+
+ sqlite3
+ gstreamer0.10-python (pygst)
+ PyQT development tools
+ python-xlib (Required for video preview plugin)

Debian and Ubuntu Linux
^^^^^^^^^^^^^^^^^^^^^^^

::

    $ sudo apt-get install -y build-essential git \
      qt4-qmake python-qt4 python-qt4-dev python-qt4-sql pyqt4-dev-tools python2.7-dev python-pip python-xlib \
      gstreamer0.10-plugins-good gstreamer0.10-plugins-bad gstreamer0.10-plugins-ugly gstreamer0.10-pulseaudio gstreamer0.10-alsa \
      python-gst0.10 python-gst0.10-dev libqt4-dev libqt4-sql libqt4-sql-sqlite

Fedora Linux
^^^^^^^^^^^^

::

    $ sudo yum install git PyQt4-devel python-pip

.. warning:: This list may be incomplete. Please :doc:`let us know </contact>` if you notice any missing packages.

Windows
^^^^^^^

.. note::  x86 version recommended whenever there is a choice.

- `python 2.7.* x86 <http://www.python.org/getit/>`_
- `setuptools-0.6c11.win32-py2.7 <https://pypi.python.org/pypi/setuptools#windows>`_
- `GStreamer-WinBuilds-GPL-x86-Beta04-0.10.7 <https://code.google.com/p/ossbuild/downloads/list>`_
- `GStreamer-WinBuilds-SDK-GPL-x86-Beta04-0.10.7 <https://code.google.com/p/ossbuild/downloads/list>`_
- `PyQt-Py2.7-x86-gpl-4.8.5-1 <http://www.riverbankcomputing.com/software/pyqt/download>`_
- `PyGTK py2.7 all-in-one <http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.24/>`_
    * Windows 32-bit packages are recommended because pygtk-all-in-one package does not have a 64-bit installer.
    * Add the following paths to your PATH variable : ```C:\Python27;C:\Python27\Lib\site-packages\PyQt4\bin```

PyPI Packages
^^^^^^^^^^^^^

You'll need to get some packages from the `Python Package Index <https://pypi.python.org/pypi>`_ (PyPI).

Upgrade to the latest version of pip::

    pip install --upgrade pip

Next, install the remaining packages. On Linux::

    pip install -Ur dev_requirements.txt

On Windows::

    pip install -Ur windows_requirements.txt


Get the source code
********************

If you plan on contributing to Freeseer, you'll need to :ref:`fork and clone the
project <fork-freeseer>`.


Running Freeseer
----------------

Once you've installed Freeseer, you can run the various tools::

    $ freeseer         # Recording UI (default when no arguments supplied)
    $ freeseer record  # Recording UI
    $ freeseer talk    # Talk Editor UI
    $ freeseer config  # Configuration UI

You can view usage with the ``-h`` or ``--help`` option::

    $ freeseer -h         # General usage
    $ freeseer record -h  # Recording usage
    $ freeseer talk -h    # Talk Editor usage
    $ freeseer config -h  # Config usage

.. note::
  If you're going to hack on Freeseer, you'll need to run it from source.
  Go into the ``src/`` directory and run it like::

    $ python -m freeseer
    $ python -m freeseer record
    $ python -m freeseer talk
    $ python -m freeseer config


Issue tracker
-------------
Found an issue? Open an issue on GitHub!

https://github.com/Freeseer/freeseer/issues


IRC channel
-----------
Drop by our `#freeseer channel <http://webchat.freenode.net/?channels=#freeseer>`_
on irc.freenode.net to chat with us.


Mailing list
------------
We have a mailing list that's also a discussion group.

http://groups.google.com/group/freeseer

Once you've joined the group, you can email subscribers at freeseer@googlegroups.com.


Authors
-------
- `Andrew Ross <https://github.com/fosslc>`_
- `Thanh Ha <https://github.com/zxiiro>`_

And many student contributors from `Google Summer of Code <http://code.google.com/soc>`_, Fedora Summer Coding,
and `Undergraduate Capstone Open Source Projects <http://ucosp.ca>`_.


Copyright and license
---------------------
© 2011-2013 FOSSLC

Licensed under the GNU General Public License, version 3 (GPLv3);
you may not use this work except in compliance with the GPLv3.

You may obtain a copy of the GPLv3 in the `LICENSE file`_, or at
http://www.fsf.org/licensing/licenses/gpl.html.

.. _LICENSE file: https://raw.github.com/Freeseer/freeseer/a0497fabdc5a548d0dea4f6fb4925aa41a6d62e8/src/LICENSE

.. rubric:: Footnotes

.. [#f1] :ref:`Requires a VGA capture device <equipment>`, also known as a
         frame grabber.
