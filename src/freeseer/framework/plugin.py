import ConfigParser

from yapsy.PluginManager import PluginManagerSingleton
from yapsy.ConfigurablePluginManager import ConfigurablePluginManager
from yapsy.IPlugin import IPlugin

class PluginManager:
    def __init__(self):
        self.plugman = PluginManagerSingleton().get()
        
        config = ConfigParser.ConfigParser()
        self.plugmanc = ConfigurablePluginManager(config, self.plugman)
        
        self.plugmanc.setPluginPlaces(["freeseer/plugins"])
        self.plugmanc.setCategoriesFilter({
            "AudioInput" : IAudioInput,
            "AudioOutput" : IAudioOutput,
            "AudioMixer" : IAudioMixer,
            "VideoInput" : IVideoInput,
            "VideoOutput" : IVideoOutput,
            "VideoMixer" : IVideoMixer,
            })
        self.plugmanc.collectPlugins()
        self.plugmanc.activatePluginByName("Video Test Source", "VideoInput", False)

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
    
class IVideoOutput(IPlugin):
    
    def get_source(self):
        pass
    
class IVideoMixer(IPlugin):
    
    def get_source(self):
        pass
