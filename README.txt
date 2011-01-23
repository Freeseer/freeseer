Freeseer is a video capture program capable of capturing desktop or vga
input and mixing it with audio to create a video. It is optimized
for capturing presentations and demonstrations at conferences.

Freeseer is written in Python, and uses Qt4 for its
GUI. It also uses Gstreamer for video/audio processing.

Our packages will handle these dependencies automatically.

Freeseer is licensed under the GPL license, version 3.
http://www.fsf.org/licensing/licenses/gpl.html

Freeseer supports free (royalty free) audio and video codecs.

-------------------------------------------------------------------------

To develop freeseer, you require:
    Make, Git, PyQT development tools

If you are pulling the code from git, then you should install
the following packages first.

On typical fresh Fedora install:
    “sudo yum install git make PyQt4-devel python-feedparser.noarch sip-devel libqxt libqxt-devel”    

On typical fresh Ubuntu install:
    “sudo apt-get install build-essential qt4-qmake pyqt4-dev-tools libqt4-dev python-qt4 python-qt4-dev python-sip python-sip-dev python2.6-dev python-feedparser”

Distros with no libQxt:
    On some distros such as Ubuntu there is no libQxt package in the repositories. In this case libQxt can be installed manually as follows.

    1. Download libqxt from http://dev.libqxt.org/libqxt/wiki/Home
    2. Unzip / Untar the package
    3. Navigate to the unpacked location
    4. Run the following command: 
        "./configure; make; sudo make install"
    5. sudo echo "/usr/local/Qxt/lib" > /etc/ld.so.conf.d/freeseer.conf
    6. sudo ldconfig

    This will install libQxt into /usr/local/Qxt. Freeseer is configured to locate libQxt libraries in /usr/local/Qxt/lib if it exists. Steps 5 and 6 tell the system where to find the libraries so they can be loaded.

-------------------------------------------------------------------------

Once you have the prerequisite componets, build freeseer by changing
directory into the src directory, and run:
    "make"

This will compile the gui files. Once this completes, you can run:
    "./freeseer"

This starts up the Freeseer GUI.

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
