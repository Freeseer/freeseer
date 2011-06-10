from freeseer.framework.plugin import IVideoInput

class VideoTestSrc(IVideoInput):
    name = "Video Test Source"
    
    def get_source(self):
        return "video test" 