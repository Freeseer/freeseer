'''
freeseer - vga/presentation capture software

Copyright (C) 2011  Free and Open Source Software Learning Centre
http://fosslc.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For support, questions, suggestions or any other inquiries, visit:
http://wiki.github.com/Freeseer/freeseer/

@author: Jordan Klassen
'''


import functools
from os import stat

from PyQt4 import QtGui, QtCore
tr = functools.partial(QtCore.QCoreApplication.translate, "metadata_filename")

from freeseer.framework.plugin import IMetadataReader

class OSStat(IMetadataReader):
    name = "os.stat Parser"
    
    # TODO: (not really important at all) create alternative using only qt calls
    fields_provided = {
        "size":IMetadataReader.header(tr("File Size"), QtCore.QString, 300),
        "date":IMetadataReader.header(tr("Date Modified"), QtCore.QDateTime, 301)} 
    
    def retrieve_metadata_internal(self, filepath):
        stdata = stat(filepath)
        return {"size":humanfilesize(stdata.st_size),
                "date":QtCore.QDateTime.fromTime_t(int(stdata.st_mtime))}

# based on gui/dialogs/qfilesystemmodel.cpp in Qt
#TODO: move this function somewhere else
def humanfilesize(nbytes):
    if nbytes == None:
        return QtCore.QString()
    # According to the Si standard KB is 1000 bytes, KiB is 1024
    # but on windows sizes are calculated by dividing by 1024 so we do what they do.
    kb = 1024
    mb = 1024 * kb
    gb = 1024 * mb
    tb = 1024 * gb
    if (nbytes >= tb):
        return QtCore.QCoreApplication.translate("QFileSystemDialog", "%1 TB").arg(QtCore.QLocale().toString(float(nbytes) / tb, 'f', 3))
    if (nbytes >= gb):
        return QtCore.QCoreApplication.translate("QFileSystemDialog", "%1 GB").arg(QtCore.QLocale().toString(float(nbytes) / gb, 'f', 2))
    if (nbytes >= mb):
        return QtCore.QCoreApplication.translate("QFileSystemDialog", "%1 MB").arg(QtCore.QLocale().toString(float(nbytes) / mb, 'f', 1))
    if (nbytes >= kb):
        return QtCore.QCoreApplication.translate("QFileSystemDialog", "%1 KB").arg(QtCore.QLocale().toString(nbytes / kb))
    return QtCore.QCoreApplication.translate("QFileSystemDialog", "%1 bytes").arg(QtCore.QLocale().toString(nbytes))

        