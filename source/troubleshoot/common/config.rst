The experimental version of Freeseer is unresponsive
----------------------------------------------------

Did you run Freeseer version 2.5.3 (or less) before running version 3?
######################################################################

The current master version is 2.5.3 and uses a different configuration than the
current experimental version (v3.0). These files are saved in a hidden folder in
the user's home directory. Freeseer-experimental will try to load the config
files that were created by Freeseer-master, and it won't work -- you'll probably
see an sqlite3 error.

To fix it, delete the `.freeseer/` directory in your home directory.
