#!/bin/sh -x

if [-f README.txt ] 
then
    cwd=`pwd`
else
    echo "Please run the deb packaging tool from the freeseer root directory."
fi

PKGROOT="${cwd}/freeseer}"
SRCROOT="${cwd}/src"
PKGTEMPLATE="${cwd}/pkg/DEBIAN"

FREESEER_PATH="/usr/shared/pyshared"
BIN_PATH="/usr/bin"

FREESEER_PYTHON_PATH="${PKGROOT}${FREESEER_PATH}"
FREESEER_BIN_PATH="${PKGROOT}${BIN_PATH}"

mkdir -p ${FREESEER_PYTHON_PATH}
mkdir -p ${FREESEER_BIN_PATH}
# TODO: add the direrctory for the icon file too

cp -R ${SRCROOT}/* ${FREESEER_PYTHON_PATH}
cp -$ ${PKGTEMPLATE}/* ${PKGROOT}

dpkg --build freeseer freeseer_2.5.3_all.deb
