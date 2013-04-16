Quick-Start Guide
=================

Freeseer by the Free and Open Source Software Learning Centre (FOSSLC)

Freeseer is a free and open source screencasting application.
Its primary purpose is capturing or streaming video at conferences.

It's been successfully used to capture presentations, demos, training material, and other videos.
It can easily handle very large conferences with many talks using varied hardware and operating systems.

It is one of a few such tools that can also record VGA output or video
from external sources such as FireWire and USB.

Freeseer is written in Python, uses Qt4 for its GUI, and Gstreamer for video/audio processing.

Freeseer is based on open standards and supports royalty free audio and video codecs.

Curious why Freeseer exists? `Read our history`_

.. _Read our history: http://fosslc.org/drupal/node/596


Documentation
-------------
Read our documentation at http://freeseer.github.com/docs


Install Freeseer from a package
-------------------------------
Use this option if you just want to run Freeseer. If you plan on developing
Freeseer, skip to the next section :ref:`install-for-dev`.

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

Visit our downloads page at https://github.com/Freeseer/freeseer/downloads

Python Package Index
********************
Freeseer can also be installed via pip::

    pip install freeseer


.. _install-for-dev:

Installing Freeseer for Development
-----------------------------------

Prerequisits
************
+ Git
+ Python 2.7+
+ sqlite3
+ gstreamer0.10-python
+ PyQT development tools
+ python-xlib (Required for video preview plugin)


Ubuntu Linux
************

::

    $ sudo apt-get install build-essential git qt4-qmake pyqt4-dev-tools libqt4-dev libqt4-sql libqt4-sql-sqlite python-qt4 python-qt4-dev python-qt4-sql python2.7-dev python-feedparser python-setuptools python-xlib
    $ sudo pip yapsy==1.9.2

Fedora Linux
************

::

    $ sudo yum install git PyQt4-devel python-feedparser.noarch python-setuptools
    $ sudo pip yapsy==1.9.2

Windows
*******

.. note::  x86 version recommended when there is a choice

* python 2.7.* x86 (http://www.python.org/getit/)
* setuptools-0.6c11.win32-py2.7 (https://pypi.python.org/pypi/setuptools#files)
* GStreamer-WinBuilds-GPL-x86-Beta04-0.10.7 (https://code.google.com/p/ossbuild/downloads/list)
* GStreamer-WinBuilds-SDK-GPL-x86-Beta04-0.10.7 (https://code.google.com/p/ossbuild/downloads/list)
* PyQt-Py2.7-x86-gpl-4.8.5-1 (http://www.riverbankcomputing.com/software/pyqt/download)
    * Windows 32-bit packages are recommended (pygtk-all-in-one package does not have a 64-bit installer yet)
    * On Windows, add the following paths to your PATH variable : ```C:\Python27;C:\Python27\Lib\site-packages\PyQt4\bin```

The following can be installed via pip::

    pip install feedparser
    pip instlal pygtk
    pip install yapsy==1.9.2

          
Git Clone Repository
********************

If your a developer and want to contribute to Freeseer clone the project with git::

    $ git clone git@github.com:Freeseer/freeseer.git


Running Freeseer
----------------

Once you have the prerequisite components you can run Freeseer using the following commands::

    $ freeseer-record  # Recording tool
    $ freeseer-config  # Configuration tool
    $ freeseer-talkeditor  # Talk-list editor

.. note:: If you are developing freeseer these scripts are in the src/ directory of the repo.


Bug tracker
-----------
Have a bug? Please create an issue here on GitHub!

https://github.com/Freeseer/freeseer/issues


IRC channel
-----------
Drop by our [#freeseer](irc://irc.freenode.net/#freeseer) channel on irc.freenode.net to get an instant response.

http://webchat.freenode.net/?channels=#freeseer


Mailing list
------------
Have a question? Ask on our mailing list!

freeseer@googlegroups.com

[Subscribe to mailing list](http://groups.google.com/group/freeseer)


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

You may obtain a copy of the GPLv3 in the `LICENSE file`_, or at:

http://www.fsf.org/licensing/licenses/gpl.html

.. _LICENSE file: https://raw.github.com/Freeseer/freeseer/a0497fabdc5a548d0dea4f6fb4925aa41a6d62e8/src/LICENSE
