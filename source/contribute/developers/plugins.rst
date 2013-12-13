Plugin Framework
================

Freeseer uses plugins so developers can easily extend the capabilities of
Freeseer in a modular fashion.

Freeseer's plugin framework is built on `Yapsy <http://yapsy.sourceforge.net>`_,
a minimal plugin system that only depends on Python's standard library.

Plugin System Setup
--------------------

Yapsy's ``PluginManager`` class provides the core logic needed to find, load,
and activate plugins. Freeseer has a ``PluginManager`` class that builds
on top of that, and can be found in ``src/freeseer/framework/plugin.py``.

Yapsy provides a ``PluginFileLocator`` class which locates plugins when they are
accessible via the filesystem. [#f1]_ Plugins are described by a text file
called the *plugin info file* which have a ".yapsy-plugin" extension by default.
But Freeseer plugins use a customized extension, ".freeseer-plugin".

.. todo:: introduce the code snippet so it's not shown as a surprise

.. code-block:: python

  from yapsy.PluginManager import PluginManagerSingleton
  from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
  ...

  class PluginManager(QtCore.QObject):
      """Freeseer's Plugin Manager provides plugin support."""

      def __init__(...):
        ...
        PluginManagerSingleton.setBehaviour([ConfigurablePluginManager])
        self.plugmanc = PluginManagerSingleton.get()
        ...
        locator = self.plugmanc.getPluginLocator()
        locator.setPluginInfoExtension("freeseer-plugin")
        ...

Freeseer searches three different directory paths for plugins:

#. User's HOME directory (``~/.freeseer/plugins/``)
#. Relative to the src directory (``src/freeseer/plugins/``)
#. If you installed Freeseer, the Python installation packages (``site-packages/freeseer/plugins/``)

Yapsy's ``IPlugin`` class defines the minimal interface needed for Yapsy
plugins. We want Freeseer's plugin classes to have a richer interface than what
``IPlugin`` provides, so we created the ``IBackendPlugin`` class in
``freeseer/framework/plugin.py`` which inherits from ``IPlugin`` and defines the
minimal interface for all Freeseer plugin classes. All Freeseer plugins should
descend from the ``IBackendPlugin`` class.

.. code-block:: python

  from yapsy.IPlugin import IPlugin
  ...

  class IBackendPlugin(IPlugin):
      """Defines the interface for all Freeseer plugins."""
      CATEGORY = "Undefined"
      ...

  class IAudioInput(IBackendPlugin):
      """A Freeseer plugin for Audio Input."""
      CATEGORY = "AudioInput"
      ...

Each class that is a descendant of the ``IPlugin`` class needs a ``CATEGORY``
attribute defined. When you are writing your own Freeseer plugin, you often
don't need to define a new category. You can extend one of the existing plugin
classes and will not need to override the ``CATEGORY`` attribute.

If you are creating a new category, you will need to override the ``CATEGORY``
attribute and add the new category name and class name to the PluginManager's
category filter in the form of a key-value pair, where the key is the
plugin's category and the value is the plugin's classname.

.. code-block:: python

  class PluginManager(QtCore.QObject):
      ...
      self.plugmanc.setCategoriesFilter({
          IAudioInput.CATEGORY: IAudioInput,
          IAudioMixer.CATEGORY: IAudioMixer,
          IVideoInput.CATEGORY: IVideoInput,
          IVideoMixer.CATEGORY: IVideoMixer,
          IImporter.CATEGORY:   IImporter,
          IOutput.CATEGORY:     IOutput})
      self.plugmanc.collectPlugins()
      ...

Yapsy provides a number of useful decorators for its PluginManager which modify
behaviour. Freeseer's plugin system uses the ``ConfigurablePluginManager`` which
allows Freeseer to save and load the active plugins and their settings to
a configuration file.

.. code-block:: python

  from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
  ...

  class PluginManager(QtCore.QObject):
      ...
      PluginManagerSingleton.setBehaviour([ConfigurablePluginManager])
      ...

Many of the Freeseer plugins, such as the video and audio plugins, use the
``ConfigurablePluginManager`` to save the active plugins.

Creating a Plugin
-----------------

The basic steps for creating a new plugin are:

#. Write a plugin info file, ``plugin_name.freeseer-plugin``, inside the
   appropriate directory within ``src/freeseer/plugins/``. This file will
   hold metadata for the plugin and has the following format::

    [Core]
    Name = Plugin Name
    Module = plugin_module_or_directory

    [Documentation]
    Author = Your Name
    Version = Latest version of Freeseer that your plugin is compatible with
    Website = http://fosslc.org
    Description = Simple one-sentence plugin description

#. Create the plugin Python file(s)

  - If you are creating a single-file plugin, create a Python module with the
    same name as your plugin info file:

  .. code-block:: none

      plugin_name.freeseer-plugin
      plugin_name.py

  - If you are creating a multi-file plugin, your Python modules should be
    separated from your plugin info file:

   1. Create a plugin directory with the same name as your plugin info file
      (minus the extension).

   2. In the new plugin directory, create the file ``__init__.py`` and write
      your plugin class inside it. Your class should extend one of the
      ``IBackendPlugin`` subclasses (e.g. ``IAudioInput``). Don't forget to
      override the class atribute ``name`` with your plugin's name.

   3. Add other useful plugin code in other modules if necessary.  For example,
      if your plugin requires a GUI, create a module called ``widget.py`` inside
      your plugin's directory and import it inside your plugin's ``__init__.py``
      module.

Accessing a Plugin
------------------

Any modules that need to access the plugins will need to import Freeseer's
``PluginManager``::

  from freeseer.framework.plugin import PluginManager

There are a number of ways to access the plugins via the ``PluginManager``. You
can iterate over all of the plugins (or all of the plugins in a given category)
or you can access a specific plugin by its name.

While Yapsy provides methods for accessing plugins (e.g. ``getAllPlugin()``,
``getPluginsOfCategory()``, and ``getPluginByName()``), the recommended way to
access the plugins is to use the accessor methods provided by Freeseer's
``PluginManager``::

  get_plugin_by_name(name, category)
  get_all_plugins()
  get_plugins_of_category(category)
  get_audioinput_plugins()
  get_audiomixer_plugins()
  get_videoinput_plugins()
  get_videomixer_plugins()
  get_importer_plugins()
  get_output_plugins()


When you call any of the above accessor methods, you receive a ``PluginInfo``
object or a list of ``PluginInfo`` objects. Such an object contains meta
information about the plugin. Each ``PluginInfo`` object has an attribute
``plugin_object`` which returns an instance of the plugin which you can then
use.

For example::

  plugman = PluginManager(config_dir)
  plugin_info = plugman.get_plugin_by_name(name, category)
  plugin = plugin_info.plugin_object
  plugin.do_something()

As another example, here's a snippet of the Freeseer codebase where a class uses
a plugin. It does so by creating an instance of the PluginManager and then calls the
plugin by name, using the ``plugin_object`` attribute to access the plugin object:

.. code-block:: python

  from freeseer.framework.plugin import PluginManager
  ...

  class QtDBConnector(object):

      def __init__(self, config_dir, ...):
          ...
          self.plugman = PluginManager(config_dir)
          ...

      ...

      def add_talks_from_rss(self, feed_url):
          """Adds talks from an RSS feed."""
          plugin = self.plugman.get_plugin_by_name("Rss FeedParser", "Importer")
          feedparser = plugin.plugin_object
          presentations = feedparser.get_presentations(feed_url)
          if presentations:
              for presentation in presentations:
                  talk = Presentation(presentation["Title"],
                                      presentation["Speaker"],
                                      presentation["Abstract"],  # Description
                                      presentation["Level"],
                                      presentation["Event"],
                                      presentation["Room"],
                                      presentation["Time"])
                  self.insert_presentation(talk)
          else:
              log.info("RSS: No data found")


.. rubric:: Footnotes

.. [#f1]
  The plugins are detected through Python, so all directories leading
  to plugins should have an ``__init__.py`` file in them.
