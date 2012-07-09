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

