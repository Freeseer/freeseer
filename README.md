Freeseer ![Freeseer](http://i.imgur.com/tqivk.png "Freeseer logo")
=========
#### by the Free and Open Source Software Learning Centre (FOSSLC)

Freeseer is a free and open source screencasting application.
Its primary purpose is capturing or streaming video at conferences.

It's been successfully used to capture presentations, demos, training material, and other videos.
It can easily handle very large conferences with many talks using varied hardware and operating systems.

It is one of a few such tools that can also record [VGA][vga-wiki] output or video
from external sources such as [FireWire][firewire-wiki], [USB][usb-wiki], [S-Video][svideo-wiki], or [RCA][rca-wiki].

Freeseer is written in Python, uses Qt4 for its GUI, and Gstreamer for video/audio processing.

Freeseer is based on open standards and supports royalty free audio and video codecs.

Curious why Freeseer exists? [Read our history!](http://fosslc.org/drupal/node/596)


Documentation
-------------
Read our documentation at http://freeseer.github.com/docs

Install from a package
----------------------
Use this option if you just want to run Freeseer. If you plan on developing
Freeseer, you would still need to fork and clone the repo.

Visit our downloads page at https://github.com/Freeseer/freeseer/downloads

**Note:** For the very latest but unstable version, you have to build from the experimental source (see developers section).


Developers
----------
### 1. Install dependencies
 + Make
 + Git
 + Python 2.7+
 + sqlite3
 + PyQT development tools
 + Passlib (for the Freeseer server tool)
 + Xlib (for one of the Linux plugins)

    ### Ubuntu Linux:

        $ sudo apt-get install build-essential qt4-qmake pyqt4-dev-tools libqt4-dev libqt4-sql libqt4-sql-sqlite python-qt4 python-qt4-dev python-qt4-sql python2.7-dev python-feedparser python-setuptools python-xlib
        $ sudo easy_install yapsy==1.9.2 passlib

    ### Fedora Linux:

        $ sudo yum install git make PyQt4-devel python-feedparser.noarch python-setuptools
        $ sudo easy_install yapsy==1.9.2

    ### Windows:
      1. [python-2.7.3](http://www.python.org/getit/)([x86](http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi) or [x64](http://www.python.org/ftp/python/2.7.3/python-2.7.3.amd64.msi))
        + Python needs to be version 2.7.\*
      1. [setuptools-0.6c11.win32-py2.7](https://pypi.python.org/pypi/setuptools#downloads) ([download](https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20))
      1. [GStreamer-WinBuilds-GPL-x86-Beta04-0.10.7](https://code.google.com/p/ossbuild/downloads/list)([download](https://ossbuild.googlecode.com/files/GStreamer-WinBuilds-GPL-x86-Beta04-0.10.7.msi))
      1. [GStreamer-WinBuilds-SDK-GPL-x86-Beta04-0.10.7](https://code.google.com/p/ossbuild/downloads/list)([download](https://ossbuild.googlecode.com/files/GStreamer-WinBuilds-SDK-GPL-x86-Beta04-0.10.7.msi))
      1. [PyQt-Py2.7-x86-gpl-4.8.5-1](http://www.riverbankcomputing.com/software/pyqt/download)([x86](http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.10/PyQt4-4.10-gpl-Py2.7-Qt4.8.4-x32.exe/download))
        + Windows 32-bit packages are recommended (pygtk-all-in-one package does not have a 64-bit installer yet)
        + On Windows, add the following paths to your PATH variable : ```C:\Python27;C:\Python27\Lib\site-packages\PyQt4\bin```
      1. these python eggs : ```pygtk```, ```feedparser```, ```yapsy```
         - ```C:\Python27\python.exe C:\Python27\Lib\site-packages\easy_install.py feedparser```
         - ```C:\Python27\python.exe C:\Python27\Lib\site-packages\easy_install.py pygtk```
         - ```C:\Python27\python.exe C:\Python27\Lib\site-packages\easy_install.py yapsy==1.9.2```

    ### Mac OS X:
    Coming soon!
          
### 2. Download
Clone the project with git:

    $ git clone git@github.com:Freeseer/freeseer.git  # Clones a copy of the master repo

### 3. Build

    $ cd freeseer
    $ make

### 4. Run

Once you have the prerequisite components you can run Freeseer using the following commands:

    $ cd src
    $ ./freeseer-record  # Recording tool
    $ ./freeseer-config  # Configuration tool
    $ ./freeseer-talkeditor  # Talk-list editor


Packaging
---------
See [PACKAGE.txt](https://github.com/Freeseer/freeseer/blob/master/PACKAGE.txt) for instructions.


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
- [Andrew Ross](https://github.com/fosslc)
- [Thanh Ha](https://github.com/zxiiro)

And many student contributors from [Google Summer of Code](http://code.google.com/soc), Fedora Summer Coding,
and [Undergraduate Capstone Open Source Projects](http://ucosp.ca).


Copyright and license
---------------------
© 2011-2012 FOSSLC

Licensed under the GNU General Public License, version 3 (GPLv3);
you may not use this work except in compliance with the GPLv3.

You may obtain a copy of the GPLv3 in the [LICENSE file][license], or at:

http://www.fsf.org/licensing/licenses/gpl.html


[rca-wiki]: http://en.wikipedia.org/wiki/RCA_connector
[svideo-wiki]: http://en.wikipedia.org/wiki/S-Video
[firewire-wiki]: http://en.wikipedia.org/wiki/FireWire_camera
[vga-wiki]: http://en.wikipedia.org/wiki/VGA_connector
[usb-wiki]: http://en.wikipedia.org/wiki/USB_video_device_class
[license]: https://raw.github.com/Freeseer/freeseer/a0497fabdc5a548d0dea4f6fb4925aa41a6d62e8/src/LICENSE

