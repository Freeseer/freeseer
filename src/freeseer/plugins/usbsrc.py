from freeseer.framework.plugin import IVideoInput

class USBSrc(IVideoInput):
    name = "USB Source"
    
    def get_name(self):
        return self.name
    
    def get_source(self):
        return "usb test" 