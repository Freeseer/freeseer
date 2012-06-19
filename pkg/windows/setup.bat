@setlocal enableextensions
@cd /d "%~dp0"

:: Remove dependencies
del /q deps

mkdir deps
cd deps

:: Download of dependencies. New dependencies should be added here.

..\wget http://ossbuild.googlecode.com/files/GStreamer-WinBuilds-GPL-x86-Beta04-0.10.7.msi
..\wget http://ossbuild.googlecode.com/files/GStreamer-WinBuilds-SDK-GPL-x86-Beta04-0.10.7.msi
..\wget http://python.org/ftp/python/2.7.2/python-2.7.2.msi
..\wget http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20
..\wget http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-Py2.7-x86-gpl-4.9.1-1.exe
..\wget http://ftp.gnome.org/pub/GNOME/binaries/win32/pygobject/2.28/pygobject-2.28.3.win32-py2.7.msi

:: Install the dependencies. Each dependency should open an installation wizard
:: Add the line corresponding to the downloaded dependency here
msiexec /i python-2.7.2.msi
msiexec /i GStreamer-WinBuilds-GPL-x86-Beta04-0.10.7.msi
msiexec /i GStreamer-WinBuilds-SDK-GPL-x86-Beta04-0.10.7.msi
msiexec /i pygobject-2.28.3.win32-py2.7.msi
setuptools-0.6c11.win32-py2.7.exe
PyQt-Py2.7-x86-gpl-4.9.1-1.exe

cd ..

cd scripts

:: Run script to modify registry to include Python and GST on Path
cscript updateEnvVariables.vbs

cd ..

:: Installing dependencies with easy_install
python C:\Python27\Lib\site-packages\easy_install.py feedparser
python C:\Python27\Lib\site-packages\easy_install.py pygtk
python C:\Python27\Lib\site-packages\easy_install.py yapsy

:: Freeseer's download and installation below is commented.
:: del freeseer
:: mkdir freeseer
:: cd freeseer

:: Download of Freeseer itself
:: ..\wget http://dl.dropbox.com/u/5695800/freeseer/freeseer-2.5.3.win32.exe

:: Install Freeseer
:: freeseer-2.5.3.win32.exe

:: cd ..

:: Change Python 2.6 => Python 2.7 on Gstreamer
xcopy /y /s "C:\Program Files\OSSBuild\GStreamer\v0.10.7\sdk\bindings\python\v2.7\lib" "C:\Program Files\OSSBuild\GStreamer\v0.10.7\lib\"
xcopy /y /s "C:\Program Files\OSSBuild\GStreamer\v0.10.7\lib\site-packages" "C:\Python27\Lib\site-packages"

:: TODO Delete the dependencies installers.

