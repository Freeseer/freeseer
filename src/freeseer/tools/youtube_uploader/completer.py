#!/usr/bin/python

import readline, glob, os

def complete(text, state):
    if os.path.isdir((glob.glob(text+'*')+[None])[state]):
        return (glob.glob(text+'*/')+[None])[state]
    else:
        return (glob.glob(text+'*')+[None])[state]

def completer():
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)