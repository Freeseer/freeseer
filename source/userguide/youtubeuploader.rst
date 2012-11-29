******************
YouTube Uploader
******************

This is a CLI tool that can upload ogg and mpg videos to YouTube. It uses a 3rd party uploader (http://code.google.com/p/youtube-upload) to upload the videos. It can upload either a single video or an entire directory. If the video is in the Freeseer ogg format then the metadata for the title and descripion will be used to populate the YouTube title and description fields. Otherwise, the title will default to the filename and the description will be blank.

Dependencies
------------------

* Must have the google api:   [https://code.google.com/p/gdata-python-client/downloads/list] (>= 1.2.4)
* Must download and install mutagen:   http://code.google.com/p/mutagen/ 
* To see the progress of the upload, it is recommended to install the progress bar (http://code.google.com/p/python-progressbar/downloads/detail?name=progressbar-2.3.tar.gz&can=2&q=)


How to Use
------------------

Run youtube-uploader in src directory to run. The user will be prompted for their email, password and filename or directory.
NOTE that when asked for the filename the freeseer record directoy is automatically used by default. So if the video is in the recording directory then you should only enter the filename

The video's url will be displayed after upload is complete.

Entering a directory will upload all videos in the directory and its sub-direcories




The folowing is the README for the upload program the uploader.py (currently in lib directory) uses:

	= Introduction =

	_Youtube-upload_ is a command-line script that uploads videos to Youtube. If a video does not comply with Youtube limitations (<15mins for a normal user) you must split it before using ffmpeg or any other tool. _Youtube-upload_ should work on any platform (GNU/Linux, BSD, OS X, Windows, ...) that runs Python.

	= Dependencies =

	  * [http://www.python.org python 2.6 or 2.7]
	  * [http://code.google.com/p/gdata-python-client python-gdata] (>= 1.2.4)

	Note: You must have logged in at least once into your Youtube account prior to uploading any videos. 

	= Download & Install =

	  * [http://code.google.com/p/youtube-upload/downloads/list Stable release]:

	{{{
	$ wget http://youtube-upload.googlecode.com/files/youtube-upload-VERSION.tgz
	$ tar xvzf youtube-upload-VERSION.tgz
	$ cd youtube-upload-VERSION
	$ sudo python setup.py install
	}}}

	  * [http://code.google.com/p/youtube-upload/source/checkout From repository]:

	{{{
	$ svn checkout http://youtube-upload.googlecode.com/svn/trunk/ youtube-upload
	$ cd youtube-upload
	$ sudo python setup.py install
	}}}

	  * If you don't want (or you can't) install software on the computer, run it directly from sources:

	{{{
	$ cd youtube-upload-VERSION
	$ python youtube_upload/youtube_upload.py ...
	}}}


	= Usage examples =

	* Upload a video:

	{{{
	$ youtube-upload --email=myemail@gmail.com --password=mypassword 
		         --title="A.S. Mutter" --description="A.S. Mutter plays Beethoven" 
		         --category=Music --keywords="mutter, beethoven" anne_sophie_mutter.flv
	www.youtube.com/watch?v=pxzZ-fYjeYs
	}}}

	* Upload the video using the Youtube API:

	{{{
	$ youtube-upload --api-upload [OTHER OPTIONS] file.flv
	}}}

	If you set explicitly the {{{--api-upload}}} options or {{{pycurl}}} isn't installed, the original Youtube API will be used to upload the video file. This method is not recommended because it does not shows the nice progressbar.

	* Upload a splited video:

	{{{
	$ youtube-upload [OPTIONS] --title="TITLE" video.part1.avi video.part2.avi
	www.youtube.com/watch?v=pxzZ-fYjeYs # title: TITLE [1/2]
	www.youtube.com/watch?v=pxzZ-fYsdff # title: TITLE [2/2]
	}}}

	* Add a video to a playlist:

	{{{
	$ youtube-upload [OPTIONS] --add-to-playlist=http://gdata.youtube.com/feeds/api/playlists/7986C428284A40A1 http://www.youtube.com/watch?v=Zpqu97l3G1U
	}}}

	Note that the argument must be the video URL (not a local file) and the playlist is the URL of the feed (with no prefix "PL").

	* Get available categories:

	{{{
	$ youtube-upload --get-categories
	Tech Education Animals People Travel Entertainment Howto Sports Autos Music News Games Nonprofit Comedy Film
	}}}

	* Split a video with _ffmpeg_

	Youtube currently limits videos to <2Gb and <15' for almost all users. You can use the Bash example script to split it before uploading:

	{{{
	$ bash examples/split_video_for_youtube.sh video.avi
	video.part1.avi
	video.part2.avi
	video.part3.avi
	}}}

	* Upload videos with _curl_

	The script uses pycurl by default (when available) to upload the video, but if you need to tweak the upload parameters take a look at the Bash script included with the sources ([http://code.google.com/p/youtube-upload/source/browse/trunk/examples/upload_with_curl.sh examples/upload_with_curl.sh]). This command, for example, would upload _somevideo.flv_ with a limit rate of 100KBytes:

	{{{
	$ youtube-upload --get-upload-form-info [OPTIONS] | bash examples/upload_with_curl.sh --limit-rate 100k
	}}}

	= Feedback =

	Use the [http://code.google.com/p/youtube-upload/issues/ issues tracker] instead to report bugs or suggest improvements.
