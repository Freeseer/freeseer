'''
Created on Nov 15, 2011

@author: jord
'''

#from freeseer.framework.plugin import IFileMetadataReader
from freeseer.framework import plugin as pluginpkg
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.PluginManager import PluginManager

class FreeseerMetadataLoader(
                             object 
#                             IFileMetadataReader
                             ):
    def __init__(self, plugin_manager):
#        IFileMetadataReader.__init__(self)
        assert isinstance(plugin_manager, pluginpkg.PluginManager)
        plugin_manager.plugmanc
        self.plugman = plugin_manager
        
    def retrieve_metadata(self, filepath):
        plugman = self.plugman.plugmanc
        assert isinstance(plugman, ConfigurablePluginManager)
        assert isinstance(plugman, PluginManager)
        data = {}
        for plugin in plugman.getPluginsOfCategory(
                pluginpkg.PluginManager.CATEGORY_METADATA):
            assert isinstance(plugin, pluginpkg.IMetadataReader)
#            if plugin.is_activated:
            if True:
                data.update(plugin.retrieve_metadata(filepath))
        return data
        
    def retrieve_metadata_batch(self, filepath_list):
        plugman = self.plugman.plugmanc
        for plugin in plugman.getPluginsOfCategory(
                pluginpkg.PluginManager.CATEGORY_METADATA):
            assert isinstance(plugin, pluginpkg.IMetadataReader)
            plugin.retrieve_metadata_batch_begin()
            
        for filepath in filepath_list:
            yield self.retrieve_metadata(filepath)
            
        for plugin in plugman.getPluginsOfCategory(
                pluginpkg.PluginManager.CATEGORY_METADATA):
            assert isinstance(plugin, pluginpkg.IMetadataReader)
            plugin.retrieve_metadata_batch_end()