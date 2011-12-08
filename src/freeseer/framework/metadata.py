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
#        assert isinstance(plugin_manager, pluginpkg.PluginManager)
#        plugin_manager.plugmanc
        self.plugman = plugin_manager
        
    def iter_active_plugins(self):
        plugman = self.plugman.plugmanc
        assert isinstance(plugman, ConfigurablePluginManager)
#        assert isinstance(plugman, PluginManager)
        for plugin in plugman.getPluginsOfCategory(
                pluginpkg.IMetadataReader.CATEGORY):
#            assert isinstance(plugin.plugin_object, pluginpkg.IMetadataReader)
#            if plugin.is_activated:
            if True:
                yield plugin.plugin_object
        
    def retrieve_metadata(self, filepath):
        data = {}
        for plugin in self.iter_active_plugins():
            data.update(plugin.retrieve_metadata(filepath))
        return data
        
    def retrieve_metadata_batch(self, filepath_list):
        for plugin in self.iter_active_plugins():
            plugin.retrieve_metadata_batch_begin()
            
        for filepath in filepath_list:
            yield self.retrieve_metadata(filepath)
            
        for plugin in self.iter_active_plugins():
            plugin.retrieve_metadata_batch_end()
            
    def get_fields(self):
        '''
        @return: dict of {str:IMetadataReader.header}
        '''
        # TODO: cache this and update when fields are changed (connect slots to see when changes occur)
        headers = {}
        for plugin in self.iter_active_plugins():
            headers.update(plugin.get_fields())
        return headers
        