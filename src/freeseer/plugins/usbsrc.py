from freeseer.framework.plugin import IVideoInput

class USBSrc(IVideoInput):
    name = "USB Source"
    
    def get_source(self):
        return "usb test" 