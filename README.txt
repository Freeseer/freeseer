Freeseer is a video capture program capable of capturing desktop or vga
input and mixing it with audio to create a video. It is optimized
for capturing presentations and demonstrations.

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

On Fedora Core:
    “sudo yum install git make PyQt4-devel”

On Ubuntu:
    “sudo apt-get install git-core pyqt4-dev-tools”

-------------------------------------------------------------------------

Once you have the prerequisite componets, build freeseer by changing
directory into the src directory, and run:
    "make"

This will compile the gui files. Once this completes, you can run:
    "./freeseer"

This starts up the Freeseer GUI.

-------------------------------------------------------------------------

Read more about hardware capture options here: 
    http://wiki.github.com/fosslc/freeseer/capture-hardware

If you wish to capture vga input using epiphan's vga2usb device:
    "sudo cp vga2usb.conf /etc/modprobe.d/"

For support, questions, suggestions or any other inquiries, visit:
    http://wiki.github.com/fosslc/freeseer/
