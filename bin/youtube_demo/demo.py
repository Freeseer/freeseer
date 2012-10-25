import os
import ConfigParser

#from freeseer.src.freeseer.frontend.configtool import configtool
#from src.freeseer.framework import config

config = ConfigParser.ConfigParser()

try:
  config.readfp(open(self.configfile))
# Config file does not exist, create a default
except IOError:
  self.writeConfig()
  #return



email = raw_input("Email address: ")
title = raw_input("Video title: ")
category = raw_input("Category (eg Music): ")
description = raw_input("Description (optional): ")
keywords = raw_input("Keywords (optional): ")
filepath = raw_input("File: ")
other = config.get('Global', 'video_directory')


os.system("python uploader.py --email="+email+" --title="+title+" --category="+category+" --description="+description+" --keywords="+keywords+" " + filepath)
