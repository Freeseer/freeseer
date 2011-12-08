'''
Created on Nov 15, 2011

@author: jord
'''

#from freeseer.framework.plugin import IFileMetadataReader
from freeseer.framework import plugin as pluginpkg
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.PluginManager import PluginManager
from PyQt4 import QtCore


class FreeseerMetadataLoader(
                             QtCore.QObject 
#                             IFileMetadataReader
                             ):
    '''
    @signal fieldsChanged() Emitted when fields are added or removed, via plugin enabling/disabling
    '''
    fields_changed = QtCore.pyqtSignal(name="fieldsChanged")
                             
    def __init__(self, plugin_manager):
        QtCore.QObject.__init__(self)
#        IFileMetadataReader.__init__(self)

#        plugin_manager.plugmanc
        self.plugman = plugin_manager
        self.headers = {}
        if self.plugman == None:
            return
        assert isinstance(plugin_manager, pluginpkg.PluginManager)
        self._cache_fields()
        
        plugin_manager.plugin_activated.connect(self.field_activated_or_deactivated)
        plugin_manager.plugin_deactivated.connect(self.field_activated_or_deactivated)
    
    
    def field_activated_or_deactivated(self, plugin_name, plugin_category):
        print(plugin_name, plugin_category)
        if plugin_category != pluginpkg.IMetadataReader.CATEGORY:
            return
        
        self._cache_fields()
        self.fields_changed.emit()
    
    def _cache_fields(self):
        headers = {}
        for plugin in self.iter_active_plugins():
            headers.update(plugin.get_fields())
        self.headers = headers
        
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
        return self.headers
    
    
        