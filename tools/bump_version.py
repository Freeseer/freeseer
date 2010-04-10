#!/usr/bin/python

import fileinput, sys

version=sys.argv[1]
files=['../src/freeseer', \
       '../src/freeseer_core.py',
       '../src/freeseer_gstreamer.py']

for f in files:
    for line in fileinput.FileInput(f, inplace=1):
        if line.startswith("__version__"):
            line = "__version__=u'" + version + "'"
        print line.rstrip()

for line in fileinput.FileInput('../setup.py', inplace=1):
    if line.startswith('      version='):
        line = "      version='" + version + "',"
    print line.rstrip()

print 'Version updated!'
