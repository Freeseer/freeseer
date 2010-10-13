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

On typical fresh Fedora Core install:
    “sudo yum install git make PyQt4-devel python-feedparser.noarch sip-devel libqxt”    

On typical fresh Ubuntu install:
    “sudo apt-get install build-essential qt4-qmake pyqt4-dev-tools libqt4-dev python-qt4 python-qt4-dev python-sip python-sip-dev python2.6-dev python-feedparser”

-------------------------------------------------------------------------

Once you have the prerequisite componets, build freeseer by changing
directory into the src directory, and run:
    "make"

This will compile the gui files. Once this completes, you can run:
    "./freeseer"

This starts up the Freeseer GUI.

--------------------------------------------------------------------------

Internationalisation

Changing languages
  To change the language simply click:
      options -> languages and select a new language from the menu

Adding a Language 

 Creating the translation files

  Go to the src folder and open the directory tools. Simply run:
    ./add_language.sh [ language_id ] 

  note: If you are running for the firs time please ensure that add_language.sh
  create_language.py and create_pro.py have their permissions set to executable.

  The language id can be either the first part of the locale id or 
  the entire locale id. Use the entire locale id if the dialect is specific
  
  Example. For a language such as english the first part 'en' would be a good choice. However for chinese
  there is a difference between zn_CN (simple) and zn_TW(Traditional). 

  The appropriate .ts file will be created in /src/freeseer/frontend/default/languages
  

 Translating the Text 

  Open the language file created with step 1 or a previously existing .ts files
  with QT Linguist. You will be prompted to select the target language and the source
  language. Select english as the source language. 

  In the context area (left side bar). Under the context MainApp there is a single word
  'language_name'. This is where you put the name of the language that will appear in the language
  menu. Note: This must be filled in, in order for the language to appear in the menu

  The instructions for using QT Linguist can be found at:
    http://doc.qt.nokia.com/4.1/linguist-translators.html  
   

 Creating the (.qm) files 

  Qt uses .qm files to translate the text at runtime. The files can be generated using 
  Qt Linguist. Once step 2 is complete, the qm file can be generated from the ts file by
  going to file -> release. This will create the .qm file with the correct name.

-------------------------------------------------------------------------

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
