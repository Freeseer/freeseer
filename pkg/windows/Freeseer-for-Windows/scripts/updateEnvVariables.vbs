' freeseer - vga/presentation capture software
'
'  Copyright (C) 2012  Free and Open Source Software Learning Centre
'  http://fosslc.org
'
'  This program is free software: you can redistribute it and/or modify
'  it under the terms of the GNU General Public License as published by
'  the Free Software Foundation, either version 3 of the License, or
'  (at your option) any later version.
'
'  This program is distributed in the hope that it will be useful,
'  but WITHOUT ANY WARRANTY; without even the implied warranty of
'  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
'  GNU General Public License for more details.
'
'  You should have received a copy of the GNU General Public License
'  along with this program.  If not, see <http://www.gnu.org/licenses/>.

' For support, questions, suggestions or any other inquiries, visit:
' http://wiki.github.com/Freeseer/freeseer/

'************************************************************
'* Modifying The System Path With New Entries *
'************************************************************
Dim ExistingPath, NewPath
Set oShell = WScript.CreateObject("WScript.Shell")
Set oEnv = oShell.Environment("SYSTEM")

Wscript.Echo oEnv("Path")

'************************************************************
'* Add your Path Entry Here *
'************************************************************
ExistingPath = oEnv("PATH")
NewPath = "C:\Python27\;C:\Program Files\OSSBuild\GStreamer\v0.10.7;" & ";" & ExistingPath
oEnv("PATH") = NewPath 'WRITE NEW PATH, INCLUDING OLD ONE

