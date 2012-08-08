:: freeseer - vga/presentation capture software
::
::  Copyright (C) 2012  Free and Open Source Software Learning Centre
::  http://fosslc.org
::
::  This program is free software: you can redistribute it and/or modify
::  it under the terms of the GNU General Public License as published by
::  the Free Software Foundation, either version 3 of the License, or
::  (at your option) any later version.
::
::  This program is distributed in the hope that it will be useful,
::  but WITHOUT ANY WARRANTY; without even the implied warranty of
::  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
::  GNU General Public License for more details.
::
::  You should have received a copy of the GNU General Public License
::  along with this program.  If not, see <http://www.gnu.org/licenses/>.

:: For support, questions, suggestions or any other inquiries, visit:
:: http://wiki.github.com/Freeseer/freeseer/

@setlocal enableextensions
@cd /d "%~dp0"

@echo off

SET "sep=^&"
SET "linebreak=VBNewLine"
SET msg1="You are about to install Freeseer and all the requirements to run it. Please notice we are on an experimental stage, so we aren't held liable if you install something that isn't really needed to run the application. The applications to be installed are listed below:"
SET msg2="Do you want to proceed with the installation?"
SET req1="- GStreamer Beta04-0.10.7"
SET req2="- Python 2.7.2"
SET req3="- Python setuptools 0.6c11"
SET req4="- PyQt4"
SET req5="- PyGObject-2.28.3"
SET req6="- Freeseer 3.0.0"
SET title="Install Freeseer's?"

ECHO WScript.Quit  MsgBox((%MSG1%%SEP%%LINEBREAK%%SEP%%LINEBREAK%%SEP%%REQ1%%SEP%%LINEBREAK%%SEP%%REQ2%%SEP%%LINEBREAK%%SEP%%REQ3%%SEP%%LINEBREAK%%SEP%%REQ4%%SEP%%LINEBREAK%%SEP%%REQ5%%SEP%%LINEBREAK%%SEP%%REQ6%%SEP%%LINEBREAK%%SEP%%LINEBREAK%%SEP%%MSG2%), vbYesNo + vbExclamation , %TITLE%) = vbYes > #.vbs
@#.vbs || goto end
EXIT
:end
@del #.vbs

@echo on

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
del /q freeseer
mkdir freeseer
cd freeseer

:: Download of Freeseer itself
..\wget http://dl.dropbox.com/u/5695800/freeseer/freeseer-3.0.0.win32.exe

:: Install Freeseer
freeseer-3.0.0.win32.exe

cd ..

:: Change Python 2.6 => Python 2.7 on Gstreamer
xcopy /y /s "%PROGRAMFILES%\OSSBuild\GStreamer\v0.10.7\sdk\bindings\python\v2.7\lib" "%PROGRAMFILES%\OSSBuild\GStreamer\v0.10.7\lib\"
xcopy /y /s "%PROGRAMFILES%\OSSBuild\GStreamer\v0.10.7\lib\site-packages" "C:\Python27\Lib\site-packages"

:: Delete the dependencies installers.
del /q deps

:: Create shortcuts to freeseer on Start Menu
mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Freeseer"
echo python C:\Python27\Scripts\freeseer-config > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Freeseer\freeseer-config.bat"
echo python C:\Python27\Scripts\freeseer-record > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Freeseer\freeseer-record.bat"
echo python C:\Python27\Scripts\freeseer-talkeditor > "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Freeseer\freeseer-talkeditor.bat"

