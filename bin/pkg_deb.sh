#!/bin/sh
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

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/fosslc/freeseer/

if [ -f README.txt ] 
then
    cwd=`pwd`
else
    echo "Please run the deb packaging tool from the freeseer root directory."
    exit 1
fi

PKGROOT="${cwd}/freeseer"
SRCROOT="${cwd}/src"
PKGTEMPLATE="${cwd}/pkg/deb"

FREESEER_PATH="/usr/shared/pyshared"
BIN_PATH="/usr/bin"

FREESEER_PYTHON_PATH="${PKGROOT}${FREESEER_PATH}"
FREESEER_BIN_PATH="${PKGROOT}${BIN_PATH}"

echo "Creating packaging directories packaging root: ${PKGROOT}"
mkdir -p ${FREESEER_PYTHON_PATH}
if [ $? -ne 0 ]
then
    echo "Could not create directory: ${FREESEER_PYTHON_PATH}"
    exit 1 
fi


mkdir -p ${FREESEER_BIN_PATH}
if [ $? -ne 0 ]
then
    echo "Could not create directory: ${FREESEER_BIN_PATH}"
    exit 1 
fi

# TODO: add the direrctory for the icon file too

echo "Copying files to our packaging root."

# TODO, make this copy better... leave out the stuff we don't want
cp -R ${SRCROOT}/* ${FREESEER_PYTHON_PATH}
if [ $? -ne 0 ]
then
    echo "Could not copy the files from ${SRCROOT} to ${FREESEER_PYTHON_PATH}"
    exit 1 
fi

# TODO: copy the executables to the bin directory

# Copy our deb packaging control file templates
cp -R ${PKGTEMPLATE}/* ${PKGROOT}
if [ $? -ne 0 ]
then
    echo "Could not copy the files from ${PKGTEMPLATE} to ${PKGROOT}"
    exit 1 
fi

# TODO: do a one-linder to update the version in the template files

echo "Generating debian package."
dpkg --build freeseer freeseer_2.5.3_all.deb
if [ $? -ne 0 ]
then
    echo "dpkg failed. Review the output to debug."
    exit 1 
fi

echo "Packaging completed successfully."

exit 0
