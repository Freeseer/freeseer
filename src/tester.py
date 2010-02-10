from freeseer_core import *

freeseer = FreeseerCore()
print freeseer.get_video_sources()
print freeseer.get_audio_sources()
print freeseer.get_talk_titles()
print freeseer.get_record_name('default')