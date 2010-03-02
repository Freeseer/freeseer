#!/usr/bin/python

import fileinput, sys

version=sys.argv[1]

for line in fileinput.FileInput("../src/freeseer-qt.py", inplace=1):
    if line.startswith("VERSION"):
        line = "VERSION=u'" + version + "'"
    print line.strip()

print 'Version updated!'
