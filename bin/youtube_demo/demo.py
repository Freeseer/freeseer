import os

email = raw_input("Email address: ")
title = raw_input("Video title: ")
category = raw_input("Category (eg Music): ")
description = raw_input("Description (optional): ")
keywords = raw_input("Keywords (optional): ")
filepath = raw_input("File Path: ")

os.system("python uploader.py --email="+email+" --title="+title+" --category="+category+" --description="+description+" --keywords="+keywords+" "+filepath)
