Freeseer 
=========
#### by Free and Open Source Software Learning Centre (FOSSLC)


![Freeseer](http://i.imgur.com/tqivk.png "Freeseer logo")

The Freeseer project is a powerful software suite for capturing or streaming video. 

It enables you to capture great presentations, demos, training material, and other videos.
It handles desktop screen-casting with ease.

It is one of a few such tools that can also record [VGA][vga-wiki] output or video
from external sources such as [FireWire][firewire-wiki], [USB][usb-wiki], [S-Video][svideo-wiki], or [RCA][rca-wiki].

It is particularly good at handling very large conferences with hundreds 
of talks and speakers using varied hardware and operating systems.

Freeseer itself can run on commodity hardware such as a laptop or desktop.
It is supported on Windows, and Linux. MacOS will be supported very soon.

Freeseer is written in Python. It uses Qt4 for its GUI and Gstreamer for video/audio processing.

Freeseer supports free (royalty free) audio and video codecs.

-------------------------------------------------------------------------


For Windows, install: 
---------------------
    - python-2.7.2
    - GStreamer-WinBuilds-GPL-x86-Beta04-0.10.7
    - GStreamer-WinBuilds-SDK-GPL-x86-Beta04-0.10.7 
    - PyQt-Py2.7-x86-gpl-4.8.5-1
    - pygtk-all-in-one-2.24.0.win32-py2.7 
    - feedparser-5.0.1 
    - setuptools-0.6c11.win32-py2.7
    - yapsy
    
    Yapsy can be installed using easy_install that comes with setuptools using the command below.
    
    Run: C:\Python27\python.exe C:\Python27\Lib\site-packages\easy_install.py yapsy
    
    NOTES:
    	- Windows 32-bit packages are recommended when installing the above packages.
    	  This is because pygtk-all-in-one package at the time of this writing does
    	  not have a 64bit installer.
    	- The above software versions are known to work well. Python does need to be version 2.7.*

          On windows, add the following paths to your PATH variable:
          C:\Python26;C:\Python26\Lib\site-packages\PyQt4\bin
          
    Troubleshooting:
    	If you have issues running freeseer with cannot import gst error this link may help:
    	http://stackoverflow.com/questions/6907473/cannot-import-gst-in-python

-------------------------------------------------------------------------

Once you have the prerequisite components you can run Freeseer using the
following commands:
        "./freeseer-record"         This is the Freeseer mainapp
        "./freeseer-config"         This is the Configuration tool
        "./freeseer-talkeditor"     This is the Talk List editor

If you would like to create packages, read PACKAGE.txt for instructions.

--------------------------------------------------------------------------

Read more about hardware capture options here: 
    http://wiki.github.com/fosslc/freeseer/capture-hardware

If you wish to capture vga input using epiphan's vga2usb device:
    first, copy the vga2usb.ko driver to /lib/modules/<kernel version>
    for the kernel you're running. Epiphan provides a list of pre-compiled
    drivers at http://epiphan.com

    Then, configure the driver:
    "sudo cp vga2usb.conf /etc/modprobe.d/; depmod -a"

For support, questions, suggestions or any other inquiries, visit:
    http://wiki.github.com/fosslc/freeseer/
  
==========================================================================

Usage
-----
Visit our download section for the latest installers:

https://github.com/fosslc/freeseer/downloads

For the cutting edge version, you have to build from the experimental source.
Note that code in the experimental branch is not guaranteed to be stable.


Developers
----------
Download the latest source code: https://github.com/fosslc/freeseer

### Build requirements
To develop and run freeseer, you require:

    Make, Git, Python 2.7, sqlite3, PyQT development tools

### Ubuntu Linux:
`$ sudo apt-get install build-essential qt4-qmake pyqt4-dev-tools libqt4-dev python-qt4 python-qt4-dev python2.6-dev python-feedparser`

### Fedora Linux:
`$ sudo yum install git make PyQt4-devel python-feedparser.noarch python-setuptools`


Bug tracker
-----------
Have a bug? Please create an issue here on GitHub!

https://github.com/fosslc/freeseer/issues


IRC channel
-----------
Drop by our [#freeseer](irc://irc.freenode.net/#freeseer) channel on irc.freenode.net

[Join via your browser](http://webchat.freenode.net/?channels=#freeseer)


Mailing list
------------
Have a question? Ask on our mailing list!

freeseer@fosslc.org

[Subscribe to mailing list](http://box674.bluehost.com/mailman/listinfo/freeseer_fosslc.org)


Authors
-------
- [Andrew Ross](https://github.com/fosslc)
- [Thanh Ha](https://github.com/zxiiro)

And many various contributors.


Copyright and license
---------------------
© 2011 FOSSLC

Licensed under the GNU General Public License, version 3 (GPLv3);
you may not use this work except in compliance with the GPLv3. You may obtain a copy of the GPLv3 in the LICENSE file, or at:

http://www.fsf.org/licensing/licenses/gpl.html


[rca-wiki]: http://en.wikipedia.org/wiki/RCA_connector
[svideo-wiki]: http://en.wikipedia.org/wiki/S-Video
[firewire-wiki]: http://en.wikipedia.org/wiki/FireWire_camera
[vga-wiki]: http://en.wikipedia.org/wiki/VGA_connector
[usb-wiki]: http://en.wikipedia.org/wiki/USB_video_device_class
