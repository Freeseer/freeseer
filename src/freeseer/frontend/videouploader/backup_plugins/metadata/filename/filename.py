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
from os import path

from PyQt4 import QtGui, QtCore
tr = functools.partial(QtCore.QCoreApplication.translate, "metadata_filename")

from freeseer.framework.plugin import IMetadataReader

class FileName(IMetadataReader):
    name = "Filename Parser"
    
    fields_provided = {"name":IMetadataReader.header(tr("File Name"), str, 100),
                       "path":IMetadataReader.header(tr("File Path"), str, 101, 
                                                     visible=False)}
    
    def retrieve_metadata_internal(self, filepath):
        return {"name":path.basename(filepath),
                "path":path.dirname(filepath)}
        