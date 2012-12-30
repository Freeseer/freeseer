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

Adding Qt Translation Files to Freeseer-monitored List:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now the developer needs to update the list of monitored translations by editing the resources file using these commands:: 
   
   cd <freeseerroot>/src/freeseer/frontend/qtcommon
   <texteditor> resource.qrc
   
The following line should be added::

   <file alias="languages/tr_LANGUAGE_LOCALE.qm">languages/tr_LANGUAGE_LOCALE.qm</file>

where LANGUAGE and LOCALE are specific to your translation. For example, an American English translation
would be::

   <file alias="languages/tr_en_US.qm">languages/tr_en_US.qm</file>.


Updating Qt Resource Files
^^^^^^^^^^^^^^^^^^^^^^^^^^

When translations are ready and complete, they need to be imported into Qt Resource files to be useful.
The good news is this is fairly easy since we include scripts to do this automatically. Simply run the
following commands::

   cd <freeseerroot>/src/freeseer/frontend/qtcommon
   make

After the above steps are followed, a sample run of Freeseer should confirm that the translation is working.


Commiting and Pushing the Translation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When all is ready to be commited please ensure that you remove the resource_rc.py files from the commit so it doesn't
cause conflicts with any other work on translation that's currently being done. You do this by checking out the original version of the file with the command below before git-adding files to be committed::

   git checkout resource_rc.py

.. note::
    This command is assumed to run from the src/freeseer/frontend/qtcommon/ directory of the Freeseer source code.

.. note::
    If you already added this file to be committed by accident you can run "git reset HEAD resource_rc.py" to reset it and then run the checkout