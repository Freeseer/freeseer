Freeseer is a video capture program capable of capturing desktop or vga
input and mixing it with audio to create a video. It is optimized
for capturing presentations and demonstrations.

Freeseer is written in Python, and uses Qt4 for its
GUI. It also uses Gstreamer for video/audio processing.

Freeseer is licensed under the GPL license, version 3.
http://www.fsf.org/licensing/licenses/gpl.html

Freeseer supports free (royalty free) audio and video codecs.

 licensed under the GPL license version 3:
http://www.fsf.org/licensing/licenses/gpl.html

To run freeseer, you require a couple of dependencies:
    Python support for Qt4
    Python support for Alsa audio sources

To do this, install the required packages as root.

On Fedora Core:
    “sudo yum install PyQt4 python-alsaaudio”

On Ubuntu:
    “sudo apt-get install python-qt4 python-alsaaudio”


Once you have the prerequisite componets, run freeseer by changing
directory into the src directory, and run:
    "./freeseer"

Read more about hardware capture options here: 
    http://wiki.github.com/fosslc/freeseer/capture-hardware

If you wish to capture vga input using epiphan's vga2usb device:
    "sudo cp vga2usb.conf /etc/modprobe.d/"

For support, questions, suggestions or any other inquiries, visit:
    http://wiki.github.com/fosslc/freeseer/
