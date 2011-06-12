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
            "AudioMixer" : IAudioMixer,
            "VideoInput" : IVideoInput,
            "VideoMixer" : IVideoMixer,
            "Output" : IOutput,
            })
        self.plugmanc.collectPlugins()
        self.plugmanc.activatePluginByName("Video Test Source", "VideoInput", False)
        self.plugmanc.activatePluginByName("Video Preview", "Output", False)
        self.plugmanc.activatePluginByName("Audio Feedback", "Output", False)
        
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
    
    def get_input(self):
        pass
    
    def get_bin(self):
        pass
