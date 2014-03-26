YouTube Uploader
================

This is a CLI tool that can upload OGG and WEBM videos to YouTube.
It can upload a single videos and/or entire directories
If the video is in the Freeseer OGG format, the metadata for the title and
descripion will be used to populate the YouTube title and description fields.
Otherwise, the title will default to the filename and the description will be a generic message.
The category is set to *Education* by default.

Dependencies
------------

* `Google Data APIs Python Client Library <https://code.google.com/p/google-api-python-client/downloads/list>`_ (≥ v1.2)
* `Mutagen <http://code.google.com/p/mutagen/downloads/list>`_ (≥ v1.20)

How to Use
----------

The Youtube Uploader has been built entirely from scratch, and uses the lastest Google Data API v3.
The latest API has fundamentally different security and authentication procedures than previous versions, for more
information on the backing technology, please see <http://oauth.net/2/>.
As such, the upload process can seem a little daunting at first glance, but in the end its actually quite easy to use,
and future features like livestreaming, could build upon this.
::


  Email (user@example.com): <user enters their youtube account email>
  Password: <user enters password>
  Video or Directory: path/to/videos <user enters file or directory to be uploaded>

If the login credentials are valid, the video(s) will be uploaded sequentially
and their URLs will be displayed.

.. note:: The video directory configured with Freeseer is used to find videos.
