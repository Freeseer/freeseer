YouTube Uploader
================

This is a CLI tool that can upload OGG and MPG videos to YouTube.
It uses `youtube-upload <http://code.google.com/p/youtube-upload>`_,
an open source tool for uploading videos from the command line.
It can upload a single video or an entire directory (including subdirectories).
If the video is in the Freeseer OGG format, the metadata for the title and
descripion will be used to populate the YouTube title and description fields.
Otherwise, the title will default to the filename and the description will be blank.
The category is set to *Education* by default.

Dependencies
------------

* `Google Data APIs Python Client Library <https://code.google.com/p/gdata-python-client/downloads/list>`_ (≥ v1.2.4)
* `Mutagen <http://code.google.com/p/mutagen/downloads/list>`_ (≥ v1.20)
* `Python Progress Bar <http://code.google.com/p/python-progressbar/downloads/list>`_ (optional, ≥ v2.3)

How to Use
----------

The youtube-uploader tool will prompt you for your email address associated with
YouTube, your password, and the path to the file or directory you want to upload.
Specifying a directory will upload all videos in that directory and its subdirectories.

::

  ./src/youtube-uploader
  Email (user@example.com): <user enters their youtube account email>
  Password: <user enters password>
  Video or Directory: path/to/videos <user enters file or directory to be uploaded>

If the login credentials are valid, the video(s) will be uploaded sequentially
and their URLs will be displayed. 

.. note:: The video directory configured with Freeseer is used to find videos.
