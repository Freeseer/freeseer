'''
Created on Nov 15, 2011

@author: jord
'''

#from freeseer.framework.plugin import IFileMetadataReader
from freeseer.framework import plugin as pluginpkg
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.PluginManager import PluginManager
from PyQt4 import QtCore
from freeseer.framework.plugin import IMetadataReader
import functools


class FreeseerMetadataLoader(pluginpkg.IMetadataReaderBase):
    '''
    This class acts as an aggregate of pluginpkg.IMetadataReader's
    
    @signal fieldsChanged() Emitted when fields are added or removed, via plugin enabling/disabling
    '''
    fields_changed = QtCore.pyqtSignal(name="fieldsChanged")
    
    field_visibility_changed = QtCore.pyqtSignal(
            "QString", bool, name="fieldVisibilityChanged")
                             
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
        
        for plugin in self.iter_active_plugins():
            self._chain_signals(plugin)
        
        plugin_manager.plugin_activated.connect(self.plugin_activated)
        plugin_manager.plugin_deactivated.connect(self.plugin_deactivated)
    
    def set_visible(self, field_id, value):
        plugin = next(p for p in self.iter_active_plugins() 
                      if p.get_fields().has_key(field_id))
        assert isinstance(plugin, IMetadataReader)
        plugin.field_visibility_changed.emit(field_id, value)
        
    def _field_visibility_changed(self, field_id, value):
        print field_id, value
        self.field_visibility_changed.emit(field_id, value)
    
    def plugin_activated_or_deactivated(self, plugin_name, plugin_category, activated):
        print(plugin_name, plugin_category)
        if plugin_category != pluginpkg.IMetadataReader.CATEGORY:
            return
        plugin = self.plugman.plugmanc.getPluginByName(plugin_name, plugin_category)
        self._chain_signals(plugin, activated)
        self._cache_fields()
        self.fields_changed.emit()
    plugin_activated = functools.partial(plugin_activated_or_deactivated, activated = True)
    plugin_deactivated = functools.partial(plugin_activated_or_deactivated, activated = False)
    
    def _cache_fields(self):
        headers = {}
        for plugin in self.iter_active_plugins():
            headers.update(plugin.get_fields())
        self.headers = headers
        
    def _chain_signals(self, plugin, connect=True):
        (plugin.field_visibility_changed.connect if connect else
         plugin.field_visibility_changed.disconnect)(self._field_visibility_changed)
        
    def iter_active_plugins(self):
#        plugman = self.plugman.plugmanc
##        assert isinstance(plugman, ConfigurablePluginManager)
##        assert isinstance(plugman, PluginManager)
#        for plugin in plugman.getPluginsOfCategory(
#                pluginpkg.IMetadataReader.CATEGORY):
##            assert isinstance(plugin.plugin_object, pluginpkg.IMetadataReader)
#            if plugin.is_activated:
#                yield plugin.plugin_object
                
        return (p.plugin_object for p in self.plugman.plugmanc.getPluginsOfCategory( 
                pluginpkg.IMetadataReader.CATEGORY) if p.is_activated)
        
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
    
        