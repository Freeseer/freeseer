Packaging guidelines for the currently supported operating systems and distributions
====================================================================================


Fedora/RedHat/CentOS/OpenSUSE Linux
------------------------------------

a) Build Freeseer using the instructions in the README.txt file
b) Create an RPM package by typing::

  python setup.py bdist_rpm --group="Sound and Video" --requires=python-feedparser, python-sqlite2,gstreamer,gstreamer-python,PyQt4

Or alternatively,

We have a handy "make rpm" target from the top level (src directory) makefile that does both steps a and b.
The::

  make rpm 

target has a dependency on building the source so this should happen automatically.


Ubuntu/Debian Linux
-------------------

Run::

  make deb

from the top level (src directory) makefile.

The "make deb" target has a dependency on building the source so this should happen automatically.


Arch Linux
----------

In order to create a package for Arch Linux, a PKGBUILD should be produced. This PKGBUILD will serve as the installer
in Arch.
The PKGBUILD currently written are likely to work without any further modifications as they take the source
code directly from Github. It's best to check on the functionality of a PKGBUILD with every new version and update
the date.

The PKGBUILD for a specific branch can be found in /pkg directory. In order to use the PKGBUILD simply download it
and run::

  makepkg

in the installation directory. This should be followed with::

  pacman -U [generated file name]

For more information about PKGBUILDs please refer to the detailed Arch Linux documentation at:: 
  
  https://wiki.archlinux.org/index.php/PKGBUILD


Windows
-------

In order to package for Windows, you require a few tools that will enable you to generate a package that
contains all prerequisites for Freeseer. Since the required software is downloaded and packaged manually, this
process will need to be done for every dependency change or Freeseer version update.

a) Build Freeseer using the instructions in the README.txt file
b) Create an MSI package by typing::

  python setup.py bdist_wininst

c) Download and install DotNetInstaller from:
  
  http://dblock.github.com/dotnetinstaller/

d) Follow the steps for a standalone bootstrapper installer from this tutorial:
  
  http://www.codeproject.com/Articles/5116/dotNetInstaller-Setup-Bootstrapper-for-NET-Applica

The added MSIs will be including all the prerequisites and the produced Freeseer MSI. It will also include 
all the easy-install python commands. An XML file will be produced (an example is in pkg/windows) which you
can modify to rearrange the installation order if needed.

e) Test the produced .exe file on a clean computer before making the package public.


Mac OS
------

Sorry, we don't support Mac OS just yet. We hope to soon.
