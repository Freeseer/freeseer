Translator
==========

We want to adapt Freeseer for as many non-native environments as possible, especially other nations and cultures.
There should be no language barrier between Freeseer and our users.
You can help in our localization efforts.


How to Contribute Translations
------------------------------

Translating Freeseer
^^^^^^^^^^^^^^^^^^^^

In order to translate Freeseer a translator can use Qt Linguist tool to read the translation files located in

    cd <freeseerroot>/src/freeseer/frontend/qtcommon/languages

In this directory there exists several *.ts files. These are the translation files for each language. Simply
load the language you would like to translate into Qt Linguist and complete the translations.

If the language you wish to translate is not available, the section `Updating Translation Files`_

Once your translation is complete simply send a pull request containing only the *.ts file that you are contributing
back.


How to update translation resources
-----------------------------------

The following steps are not required for a translator but more for a developer to make new translation contributions
appear in freeseer.

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
