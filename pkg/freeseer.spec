#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# spec file for freeseer rpm package

%define _bindir		%kde_path/bin
%define _datadir	%kde_path/share
%define _iconsdir	%_datadir/icons
%define _docdir		%_datadir/doc
%define _localedir	%_datadir/locale
%define qt_path		/usr/lib/qt3

%define packer %(finger -lp `echo "$USER"` | head -n 1 | cut -d: -f 3)

Name:      freeseer
Summary:   Freeseer, video studio in a backpack.
Version:   1.9.7
Release:   blah
License:   GPLv3
Vendor:    FOSSLC Mailing List <freeseer@fosslc.org>
Packager:  %packer
Group:     Sound and Video
Source0:   %{name}2-%version.tar.gz
BuildRoot: %{_tmppath}/%{name}2-%{version}-%{release}-build
BuildRequires: 
Prereq: /usr/bin/make

%description
This project contains code for a video capture utility capable of capturing presentations. It captures vga output and audio and mixes them together to produce a video thus enabling you to capture great presentations, demos, or training material easily.

Read more at: http://wiki.github.com/fosslc/freeseer/

%package freeseer
Requires: PyQt4 python-alsaaudio
Summary: Freeseer video capture suite
Group: Sound and Video
Provides: freeseer

%description freeseer
This package contains necessary files for the Freeeseer video capture suite .

 
%prep
echo Building %{name}-%{version}-%{release}

%build
make

%install
make DESTDIR=%buildroot install

%clean
[ ${RPM_BUILD_ROOT} != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%post

%postun

%files
%defattr(-,root,root)

%dir %_docdir/HTML/en/%{name}2/
%doc %_docdir/HTML/*/%{name}2/*.docbook
%doc %_docdir/HTML/*/%{name}2/*.png
%doc %_docdir/HTML/*/%{name}2/index.cache.bz2

# the binary files
%{_bindir}/%{name}
%{_bindir}/%{name}2

# the shared libraries
%kde_path/%_lib/*.so.*.*.*

#
%dir %_datadir/apps/
%dir %_datadir/apps/%{name}2/
%dir %_datadir/apps/%{name}2/html
%dir %_datadir/apps/%{name}2/templates
%dir %_datadir/apps/%{name}2/templates/C
%dir %_datadir/apps/%{name}2/templates/de_DE
%dir %_datadir/apps/%{name}2/templates/en_GB
%dir %_datadir/apps/%{name}2/templates/en_US
%dir %_datadir/apps/%{name}2/templates/fr_FR
%dir %_datadir/apps/%{name}2/templates/pt_BR
%dir %_datadir/apps/%{name}2/templates/ru_SU
%_datadir/apps/%{name}2/templates/README
%_datadir/apps/%{name}2/templates/*/*.kmt

%_datadir/apps/%{name}2/*rc
%_datadir/apps/%{name}2/html/*
%_datadir/apps/%{name}2/tips

%dir %_datadir/apps/%{name}2/pics/
%_datadir/apps/%{name}2/pics/*.png

%dir %_datadir/apps/%{name}2/icons/
%dir %_datadir/apps/%{name}2/icons/hicolor/
%dir %_datadir/apps/%{name}2/icons/hicolor/16x16/
%dir %_datadir/apps/%{name}2/icons/hicolor/16x16/actions/
%dir %_datadir/apps/%{name}2/icons/hicolor/22x22/
%dir %_datadir/apps/%{name}2/icons/hicolor/22x22/actions/
%dir %_datadir/apps/%{name}2/icons/hicolor/32x32/
%dir %_datadir/apps/%{name}2/icons/hicolor/32x32/apps
%dir %_datadir/apps/%{name}2/icons/hicolor/48x48/
%dir %_datadir/apps/%{name}2/icons/hicolor/48x48/apps
%dir %_datadir/apps/%{name}2/icons/hicolor/64x64/
%dir %_datadir/apps/%{name}2/icons/hicolor/64x64/apps
%_datadir/apps/%{name}2/icons/hicolor/*/*/*.png

%_datadir/applications/kde/kmymoney2.desktop
%_datadir/mimelnk/application/x-kmymoney2.desktop
%_datadir/servicetypes/*

%_iconsdir/*/*/*/*.png

%doc %_mandir/man1/kmymoney2.1.gz

%_localedir/*/*/*.mo

%files freeseer
%_datadir/services/kmm_ofximport.desktop
%kde_path/%_lib/kde3/kmm_ofximport.so

%changelog
* Fri Apr 2 2010 - fosslc (at) gmail.com
- Initial package
