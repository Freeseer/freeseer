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

WAROOT="${cwd}"
PKGROOT="${cwd}/freeseer"
SRCROOT="${cwd}/src"
PKGTEMPLATE="${cwd}/pkg/deb"

PYTHON_PATH="/usr/shared/pyshared"
BIN_PATH="/usr/bin"
PIXMAPS_PATH="/usr/share/pixmaps"
DESKTOP_PATH="/usr/share/applications"

PKGROOT_PYTHON_PATH="${PKGROOT}${PYTHON_PATH}"
PKGROOT_BIN_PATH="${PKGROOT}${BIN_PATH}"
PKGROOT_PIXMAPS_PATH="${PKGROOT}${PIXMAPS_PATH}"
PKGROOT_DESKTOP_PATH="${PKGROOT}${DESKTOP_PATH}"

for NEW_PATH in "${PKGROOT_PYTHON_PATH}" "${PKGROOT_BIN_PATH}" "${PKGROOT_PIXMAPS_PATH}" "${PKGROOT_DESKTOP_PATH}"
do
    echo "Creating packaging directories packaging root: ${NEW_PATH}"
    mkdir -p ${NEW_PATH}
    if [ $? -ne 0 ]
    then
        echo "Could not create directory: ${NEW_PATH}"
        exit 1 
    fi
done

# set up a simple script in the bin directory
# this calls the actual executable
for exec in "freeseer-record" "freeseer-config" "freeseer-talkeditor"
do
  echo "#!/bin/sh\n${PYTHON_PATH}/${exec}" > "${PKGROOT_BIN_PATH}/${exec}"
  chmod 755 "${PKGROOT_BIN_PATH}/${exec}"
done

echo "Copying files to our packaging root."

# copy the desktop entry
cp -R ${WAROOT}/pkg/desktop/freeseer.desktop ${PKGROOT_DESKTOP_PATH}
if [ $? -ne 0 ]
then
    echo "Could not copy the files from ${SRCROOT} to ${PKGROOT_PYTHON_PATH}"
    exit 1 
fi

# Copy the icon
cp -R ${SRCROOT}/freeseer/framework/resources/freeseer_logo.png ${PKGROOT_PIXMAPS_PATH}
if [ $? -ne 0 ]
then
    echo "Could not copy the files from ${SRCROOT} to ${PKGROOT_PYTHON_PATH}"
    exit 1 
fi


# TODO, make this copy better... leave out the stuff we don't want
cp -R ${SRCROOT}/* ${PKGROOT_PYTHON_PATH}
if [ $? -ne 0 ]
then
    echo "Could not copy the files from ${SRCROOT} to ${PKGROOT_PYTHON_PATH}"
    exit 1 
fi

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
