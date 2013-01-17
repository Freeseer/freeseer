Translator
==========

We want to adapt Freeseer for as many non-native environments as possible, especially other nations and cultures.
There should be no language barrier between Freeseer and our users.
You can help in our localization efforts.


Add a Translation
-----------------

1. Open the **Qt Linguist** tool --
   it should come with your installation of **PyQt**

2. Translation files are located in
   ``<path-to-freeseer>/src/freeseer/frontend/qtcommon/languages/``.
   If a file for your language exists, continue to step 3.
   Otherwise, you'll need to `update translation resources`_ first.


3. Using Qt Linguist, open a translation (``.ts``) file for your language
  
4. Once you've completed the translation, `send a pull request
   <https://help.github.com/articles/creating-a-pull-request>`_
   containing only the ``.ts`` file(s) that you modified.

.. seealso::
  `Qt Linguist documentation for translators
  <http://doc.qt.digia.com/qt/linguist-translators.html>`_


Update Translation Resources
----------------------------

For new translations to appear in Freeseer, you need to update the translation
resources. This task is typically left to a developer, not a translator.
Please ask a developer to update the translation resources before you attempt to.

1. Update Translation Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This step only needs to be completed if a developer wrote code that contains
new translation strings in the user-interface. To update translation files::

   cd <path-to-freeseer>/src/freeseer/frontend/qtcommon/languages
   pylupdate4 freeseer.pro
  
The ``freeseer.pro`` file specifies which source files contain translation
strings, as well as which translation files need to be updated and/or created.
If you want to translate to a new language, add a new locale for that language.

2. Add Qt Translation Files to Freeseer-monitored List
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, you need to update the list of monitored translations by editing the
``resource.qrc`` file:: 
   
   cd <path-to-freeseer>/src/freeseer/frontend/qtcommon
   <text-editor> resource.qrc
   
Add the following line::

   <file alias="languages/tr_LANGUAGE_LOCALE.qm">languages/tr_LANGUAGE_LOCALE.qm</file>

where `LANGUAGE` and `LOCALE` are specific to your translation.
For example, for an American English translation::

   <file alias="languages/tr_en_US.qm">languages/tr_en_US.qm</file>


3. Update Qt Resource Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^

When translations are ready to be used, they need to be imported into Qt's resource files.
We included a script to automate the process. Simply run::

   cd <path-to-freeseer>/src/freeseer/frontend/qtcommon
   make

You should now see your translation(s) the next time you run Freeseer.
