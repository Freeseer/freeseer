import ConfigParser
import os

from yapsy.PluginManager import PluginManagerSingleton
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.IPlugin import IPlugin

class PluginManager:
    def __init__(self, configdir):
        plugman = PluginManagerSingleton().get()
        
        self.configdir = configdir
        self.configfile = os.path.abspath("%s/plugin.conf" % self.configdir)
        
        self.config = ConfigParser.ConfigParser()
        self.load()
        self.plugmanc = ConfigurablePluginManager(self.config, self, plugman)
        
        self.plugmanc.setPluginPlaces(["freeseer/plugins"])
        self.plugmanc.setCategoriesFilter({
            "AudioInput" : IAudioInput,
            "AudioMixer" : IAudioMixer,
            "VideoInput" : IVideoInput,
            "VideoMixer" : IVideoMixer,
            "Output" : IOutput,
            })
        self.plugmanc.collectPlugins()
#        self.plugmanc.activatePluginByName("Video Test Source", "VideoInput", False)
#        self.plugmanc.activatePluginByName("Video Preview", "Output", False)
#        self.plugmanc.activatePluginByName("Audio Feedback", "Output", False)
        
    def __call__(self):
        pass
    
    def load(self):
        try:
            self.config.readfp(open(self.configfile))
        # Config file does not exist, create a default
        except IOError:
            self.save()
            return
        
    def save(self):
        with open(self.configfile, 'w') as configfile:
            self.config.write(configfile)
        
    def activate_plugin(self, plugin_name, plugin_category):
        self.plugmanc.activatePluginByName(plugin_name, plugin_category, True)
        self.save()
        print 'here'
        
    def deactivate_plugin(self, plugin_name, plugin_category):
        self.plugmanc.deactivatePluginByName(plugin_name, plugin_category, True)
        self.save()
        
    def get_output_plugins(self):
        return None

class IAudioInput(IPlugin):
    
    def get_source(self):
        pass
    
class IAudioOutput(IPlugin):
    
    def get_source(self):
        pass
    
class IAudioMixer(IPlugin):
    
    def get_source(self):
        pass
    
class IVideoInput(IPlugin):
    
    def get_source(self):
        pass
    
class IVideoMixer(IPlugin):
    
    def get_source(self):
        pass

class IOutput(IPlugin):
    name = None
    type = None # Types: audio, video, both
    
    def get_name(self):
        return self.name
    
    def get_type(self):
        return self.type
    
    def get_output_bin(self):
        pass
