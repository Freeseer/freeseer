Translator
==========

We want to adapt Freeseer for as many non-native environments as possible, especially other nations and cultures.
There should be no language barrier between Freeseer and our users.
You can help in our localization efforts.


How to Contribute Translations
------------------------------

*TODO:* https://github.com/Freeseer/freeseer/issues/127

How to update translation resources
-----------------------------------

There are 2 items to keep in mind in relation to updating translation resources.

1. Updating Translation Files
2. Updating Qt Resource Files

Updating Translation Files
^^^^^^^^^^^^^^^^^^^^^^^^^^

The first item needs to be done when a developer writes new code in the software and thus adding new translation
strings to the software which needs to be translated. To update translation files run the following commands::

   cd <freeseerroot>/src/freeseer/frontend/qtcommon/languages
   pylupdate4 freeseer.pro
  
The freeseer.pro file contains details regarding which source files contain translation strings as well as which
translation files need to be updated and/or created. If you wish to translate a new langauge simply add a new locale
for the language you wish to translate.

Updating Qt Resource Files
^^^^^^^^^^^^^^^^^^^^^^^^^^

When translations are ready and complete, they need to be imported into Qt Resource files to be useful.
The good news is this is fairly easy since we include scripts to do this automatically. Simply run the
following commands::

   cd <freeseerroot>/src/freeseer/frontend/qtcommon
   make