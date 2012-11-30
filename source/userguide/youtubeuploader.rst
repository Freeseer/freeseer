******************
YouTube Uploader
******************

This is a CLI tool that can upload ogg and mpg videos to YouTube. It uses `youtibe-upload <http://code.google.com/p/youtube-upload>`_, an open source tool for uploading videos from the command line, to upload the videos. It can upload either a single video or an entire directory. If the video is in the Freeseer ogg format then the metadata for the title and descripion will be used to populate the YouTube title and description fields. Otherwise, the title will default to the filename and the description will be blank. Also, the category is set to Education by default.

Dependencies
------------------

* `Google Data APIs Python Client Library <https://code.google.com/p/gdata-python-client/downloads/list>`_ (>= 1.2.4)
* `Mutagen <http://code.google.com/p/mutagen/downloads/list>`_ (>=1.20)
* `Python Progress Bar <http://code.google.com/p/python-progressbar/downloads/list>`_ (optional, >= 2.3)



How to Use
------------------

The youtube-uploader tool will prompt you for your email address associated with YouTube, your password, and the path to the file or directory you want to upload. Specifying a directory will upload all videos in that directory and its subdirectories. Video URLs will appear after a successful upload. Note that youtube-uploader opens your Freeseer video directory to find videos::

	cd src/
	./youtube-uploader
	Email (user@example.com): *user enters their youtube account email
	Password: *user enters password
	Video or Directory: path/to/videos *user enters file or directory to be uploaded

	If email/password match then video(s) will be uploaded and its url is displayed. 

