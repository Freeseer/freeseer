'''
freeseer - vga/presentation capture software

Copyright (C) 2011-2013  Free and Open Source Software Learning Centre
http://fosslc.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For support, questions, suggestions or any other inquiries, visit:
http://wiki.github.com/Freeseer/freeseer/

@author: Jonathan Shen
'''

import ConfigParser

import pygst
pygst.require("0.10")
import gst
import logging
import httplib
import simplejson
import pickle
import webbrowser

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IOutput

from oauth import oauth

class RTMPOutput(IOutput):

    name = "RTMP Streaming"
    os = ["linux", "linux2", "win32", "cygwin"]
    type = IOutput.BOTH
    recordto = IOutput.STREAM
    tags = None
    
    # RTMP Streaming variables
    url = ""
    audio_quality = 0.3
    video_bitrate = 2400
    video_tune='none'
    audio_codec='lame'
    streaming_dest='custom'
    streaming_key = ''
    consumer_key = ''
    consumer_secret = ''
    authorization_url = ''

    TUNE_VALUES = ['none', 'film', 'animation', 'grain', 'stillimage', 'psnr', 'ssim', 'fastdecode', 'zerolatency']
    AUDIO_CODEC_VALUES = ['lame', 'faac']
    STREAMING_DESTINATION_VALUES = ['custom', 'justin.tv']
    JUSTIN_URL = 'rtmp://live-3c.justin.tv/app/'
    STATUS_KEYS = ['artist', 'title']
    DESCRIPTION_KEY = 'comment'

    justin_api = None
    justin_api_persistent = ''
    
	#@brief - RTMP Streaming plugin.
	# Structure for function was based primarily off the ogg function
	# Creates a bin to stream flv content to [self.url]
	# Bin has audio and video ghost sink pads 
	# Converts audio and video to flv with [flvmux] element
	# Streams flv content to [self.url]
	# TODO - Error handling - verify pad setup
    def get_output_bin(self, audio=True, video=True, metadata=None):
        bin = gst.Bin()
        
        if metadata is not None:
            self.set_metadata(metadata)

        # Muxer
        muxer = gst.element_factory_make("flvmux", "muxer")
        
        # Setup metadata
        # set tag merge mode to GST_TAG_MERGE_REPLACE
        merge_mode = gst.TagMergeMode.__enum_values__[2]
    
        muxer.merge_tags(self.tags, merge_mode)
        muxer.set_tag_merge_mode(merge_mode)
        
        bin.add(muxer)
        
        url = self.url
        audio_codec = self.audio_codec
        
        # RTMP sink
        rtmpsink = gst.element_factory_make('rtmpsink', 'rtmpsink')
        rtmpsink.set_property('location', url)
        bin.add(rtmpsink)
        
        #
        # Setup Audio Pipeline if Audio Recording is Enabled
        #
        if audio:
            audioqueue = gst.element_factory_make("queue", "audioqueue")
            bin.add(audioqueue)
            
            audioconvert = gst.element_factory_make("audioconvert", "audioconvert")
            bin.add(audioconvert)
            
            audiolevel = gst.element_factory_make('level', 'audiolevel')
            audiolevel.set_property('interval', 20000000)
            bin.add(audiolevel)
            
            audiocodec = gst.element_factory_make(audio_codec, "audiocodec")
            
            if 'quality' in audiocodec.get_property_names():
                audiocodec.set_property("quality", int(self.audio_quality))
            else:
                logging.debug("WARNING: Missing property: 'quality' on audiocodec; available: " + \
                    ','.join(audiocodec.get_property_names()))
            bin.add(audiocodec)
            
            # Setup ghost pads
            audiopad = audioqueue.get_pad("sink")
            audio_ghostpad = gst.GhostPad("audiosink", audiopad)
            bin.add_pad(audio_ghostpad)
            
            # Link Elements
            audioqueue.link(audioconvert)
            audioconvert.link(audiolevel)
            audiolevel.link(audiocodec)
            audiocodec.link(muxer)
        
        
        #
        # Setup Video Pipeline
        #
        if video:
            videoqueue = gst.element_factory_make("queue", "videoqueue")
            bin.add(videoqueue)
            
            videocodec = gst.element_factory_make("x264enc", "videocodec")
            videocodec.set_property("bitrate", int(self.video_bitrate))
            if self.video_tune != 'none':
            	videocodec.set_property('tune', self.video_tune)
            bin.add(videocodec)
            
            # Setup ghost pads
            videopad = videoqueue.get_pad("sink")
            video_ghostpad = gst.GhostPad("videosink", videopad)
            bin.add_pad(video_ghostpad)
            
            # Link Elements
            videoqueue.link(videocodec)
            videocodec.link(muxer)
        
        #
        # Link muxer to rtmpsink
        #
        muxer.link(rtmpsink)

        self.justin_api.set_channel_status(self.get_talk_status(metadata),
                                                self.get_description(metadata))

        return bin

    def get_talk_status(self, metadata):
        if not metadata: return ""
        return " - ".join([metadata[status_key] for status_key in self.STATUS_KEYS])
    
    def get_description(self, metadata):
        if not metadata: return ""
        return metadata[self.DESCRIPTION_KEY]
    
    def set_metadata(self, data):
        '''
        Populate global tag list variable with file metadata for
        vorbistag audio element
        '''
        self.tags = gst.TagList()

        for tag in data.keys():
            if(gst.tag_exists(tag)):
                self.tags[tag] = data[tag]
            else:
                #self.core.logger.log.debug("WARNING: Tag \"" + str(tag) + "\" is not registered with gstreamer.")
                pass
            
    def load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.url = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Stream URL")
            self.audio_quality = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Quality")
            self.video_bitrate = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Video Bitrate")
            self.video_tune = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Video Tune")
            self.audio_codec = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Codec")
            self.streaming_key = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "justin.tv Streaming Key")
            self.consumer_key = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "justin.tv Consumer Key")
            self.consumer_secret = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "justin.tv Consumer Secret")
            self.streaming_dest = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Streaming Destination")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Stream URL", self.url)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Quality", self.audio_quality)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Bitrate", self.video_bitrate)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Tune", self.video_tune)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Codec", self.audio_codec)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "justin.tv Streaming Key", self.streaming_key)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "justin.tv Consumer Key", self.consumer_key)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "justin.tv Consumer Secret", self.consumer_secret)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Streaming Destination", self.streaming_key)

        try:
            self.justin_api_persistent = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "justin.tv API Persistent Object")
            if self.justin_api_persistent:
                self.justin_api = JustinApi.from_string(self.justin_api_persistent)
                self.justin_api.set_save_method(self.set_justin_api_persistent)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "justin.tv API Persistent Object", self.justin_api_persistent)

    def get_content_widget(self, streaming_dest):
        if streaming_dest == self.STREAMING_DESTINATION_VALUES[0]:
            self.custom_widget = QtGui.QWidget()
            self.custom_widget_layout = QtGui.QFormLayout()
            self.custom_widget.setLayout(self.custom_widget_layout)
            #
            # Stream URL
            #
            
            # TODO: URL validation?
            
            self.label_stream_url = QtGui.QLabel("Stream URL")
            self.lineedit_stream_url = QtGui.QLineEdit()
            self.custom_widget_layout.addRow(self.label_stream_url, self.lineedit_stream_url)

            self.lineedit_stream_url.textEdited.connect(self.set_stream_url)
            
            #
            # Audio Quality
            #
            
            self.label_audio_quality = QtGui.QLabel("Audio Quality")
            self.spinbox_audio_quality = QtGui.QSpinBox()
            self.spinbox_audio_quality.setMinimum(0)
            self.spinbox_audio_quality.setMaximum(9)
            self.spinbox_audio_quality.setSingleStep(1)
            self.spinbox_audio_quality.setValue(5)
            self.custom_widget_layout.addRow(self.label_audio_quality, self.spinbox_audio_quality)
            
            self.custom_widget.connect(self.spinbox_audio_quality, QtCore.SIGNAL('valueChanged(int)'), self.set_audio_quality)

            #
            # Audio Codec
            #
            
            self.label_audio_codec = QtGui.QLabel("Audio Codec")
            self.combobox_audio_codec = QtGui.QComboBox()
            self.combobox_audio_codec.addItems(self.AUDIO_CODEC_VALUES)
            self.custom_widget_layout.addRow(self.label_audio_codec, self.combobox_audio_codec)
            
            self.custom_widget.connect(self.combobox_audio_codec, 
                                QtCore.SIGNAL('currentIndexChanged(const QString&)'), 
                                self.set_audio_codec)
            
            #
            # Video Quality
            #
            
            self.label_video_quality = QtGui.QLabel("Video Quality (kb/s)")
            self.spinbox_video_quality = QtGui.QSpinBox()
            self.spinbox_video_quality.setMinimum(0)
            self.spinbox_video_quality.setMaximum(16777215)
            self.spinbox_video_quality.setValue(2400)           # Default value 2400
            self.custom_widget_layout.addRow(self.label_video_quality, self.spinbox_video_quality)
            
            self.custom_widget.connect(self.spinbox_video_quality, QtCore.SIGNAL('valueChanged(int)'), self.set_video_bitrate)
            
            #
            # Video Tune
            #
            
            self.label_video_tune = QtGui.QLabel("Video Tune")
            self.combobox_video_tune = QtGui.QComboBox()
            self.combobox_video_tune.addItems(self.TUNE_VALUES)
            self.custom_widget_layout.addRow(self.label_video_tune, self.combobox_video_tune)
            
            self.custom_widget.connect(self.combobox_video_tune, 
                                QtCore.SIGNAL('currentIndexChanged(const QString&)'), 
                                self.set_video_tune)
            
            #
            # Note
            #
            
            self.label_note = QtGui.QLabel(self.gui.uiTranslator.translate('rtmp', "*For RTMP streaming, all other outputs must be set to leaky"))
            self.custom_widget_layout.addRow(self.label_note)

            self.content_widget = self.custom_widget
            self.load_config_delegate = self.custom_widget_load_config

        if streaming_dest == self.STREAMING_DESTINATION_VALUES[1]:
            self.justin_widget = QtGui.QWidget()
            self.justin_widget_layout = QtGui.QFormLayout()
            self.justin_widget.setLayout(self.justin_widget_layout)

            #
            # justin.tv Streaming Key
            #
            
            self.label_streaming_key = QtGui.QLabel("Streaming Key")
            self.lineedit_streaming_key = QtGui.QLineEdit()
            self.justin_widget_layout.addRow(self.label_streaming_key, self.lineedit_streaming_key)

            self.lineedit_streaming_key.textEdited.connect(self.set_streaming_key)

            #
            # Note
            #
            
            self.label_note = QtGui.QLabel(self.gui.uiTranslator.translate('rtmp', "*See: http://www.justin.tv/broadcast/adv_other\nYou must be logged in to obtain your Streaming Key"))
            self.justin_widget_layout.addRow(self.label_note)

            #
            # Consumer key
            #

            self.label_consumer_key = QtGui.QLabel("Consumer Key (optional)")
            self.lineedit_consumer_key = QtGui.QLineEdit()
            self.justin_widget_layout.addRow(self.label_consumer_key, self.lineedit_consumer_key)

            self.lineedit_consumer_key.textEdited.connect(self.set_consumer_key)

            #
            # Consumer key
            #

            self.label_consumer_secret = QtGui.QLabel("Consumer Secret (optional)")
            self.lineedit_consumer_secret = QtGui.QLineEdit()
            self.justin_widget_layout.addRow(self.label_consumer_secret, self.lineedit_consumer_secret)

            self.lineedit_consumer_secret.textEdited.connect(self.set_consumer_secret)

            #
            # Apply button, so as not to accidentally overwrite custom settings
            #
            
            self.apply_button = QtGui.QPushButton("Apply")
            self.apply_button.setToolTip(self.gui.uiTranslator.translate('rtmp', "Overwrite custom settings for justin.tv"))
            self.justin_widget_layout.addRow(self.apply_button)

            self.apply_button.clicked.connect(self.apply_justin_settings)

            self.content_widget = self.justin_widget
            self.load_config_delegate = self.justin_widget_load_config

        return self.content_widget
    
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            self.widget.setWindowTitle("RTMP Streaming Options")
            
            self.widget_layout = QtGui.QFormLayout()
            self.widget.setLayout(self.widget_layout)

            #
            # Streaming presets
            #

            self.label_streaming_dest = QtGui.QLabel("Streaming Destination")
            self.combobox_streaming_dest = QtGui.QComboBox()
            self.combobox_streaming_dest.addItems(self.STREAMING_DESTINATION_VALUES)
            
            self.widget_layout.addRow(self.label_streaming_dest, self.combobox_streaming_dest)
            
            self.widget.connect(self.combobox_streaming_dest,
                                QtCore.SIGNAL('currentIndexChanged(const QString&)'),
                                self.set_streaming_dest)

            self.scroll_area = QtGui.QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.widget_layout.addRow(self.scroll_area)
            
            self.scroll_area.setWidget(self.get_content_widget(self.streaming_dest))

        return self.widget

    def load_config_delegate(self):
        pass

    def widget_load_config(self, plugman):
        self.load_config(plugman)
        self.load_config_delegate()

    def justin_widget_load_config(self):
        self.lineedit_streaming_key.setText(self.streaming_key)
        self.lineedit_consumer_key.setText(self.consumer_key)
        self.lineedit_consumer_secret.setText(self.consumer_secret)

    def custom_widget_load_config(self):
        self.lineedit_stream_url.setText(self.url)

        self.spinbox_audio_quality.setValue(float(self.audio_quality))
        self.spinbox_video_quality.setValue(int(self.video_bitrate))

        tuneIndex = self.combobox_video_tune.findText(self.video_tune)
        self.combobox_video_tune.setCurrentIndex(tuneIndex)
        
        acIndex = self.combobox_audio_codec.findText(self.audio_codec)
        self.combobox_audio_codec.setCurrentIndex(acIndex)

    def set_stream_url(self, text):
        self.url = text
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Stream URL", self.url)
        
    def set_audio_quality(self):
        self.audio_quality = self.spinbox_audio_quality.value()
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Quality", str(self.audio_quality))
        
    def set_video_bitrate(self):
        self.video_bitrate = self.spinbox_video_quality.value()
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Bitrate", str(self.video_bitrate))
        
    def set_video_tune(self, tune):
        self.video_tune = tune
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Tune", str(self.video_tune))
        self.plugman.save()

    def set_audio_codec(self, codec):
        self.audio_codec = codec
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Audio Codec", str(self.audio_codec))
        self.plugman.save()

    def set_streaming_dest(self, dest):
        self.streaming_dest = dest
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Streaming Destination", str(self.streaming_dest))
        self.plugman.save()

        if str(self.streaming_dest) in self.STREAMING_DESTINATION_VALUES:
            index = min([i for i in range(len(self.STREAMING_DESTINATION_VALUES)) \
                if self.STREAMING_DESTINATION_VALUES[i] == self.streaming_dest])
            self.combobox_streaming_dest.setCurrentIndex(index)

        self.scroll_area.setWidget(None)
        self.scroll_area.setWidget(self.get_content_widget(self.streaming_dest))
        self.load_config_delegate()

    def set_streaming_key(self, text):
        self.streaming_key = str(text)
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "justin.tv Streaming Key", self.streaming_key)
        self.plugman.save()

    def set_consumer_key(self, text):
        self.consumer_key = str(text)
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "justin.tv Consumer Key", self.consumer_key)
        self.plugman.save()

    def set_consumer_secret(self, text):
        self.consumer_secret = str(text)
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "justin.tv Consumer Secret", self.consumer_secret)
        self.plugman.save()

    def set_justin_api_persistent(self, text):
        self.justin_api_persistent = str(text)
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "justin.tv API Persistent Object", self.justin_api_persistent)
        self.plugman.save()

    def apply_justin_settings(self):
        # here is where all the justin.tv streaming presets will be applied
        self.set_stream_url(self.JUSTIN_URL + self.streaming_key)
        self.set_audio_codec('lame')
        try:
            if self.consumer_key and self.consumer_secret:
                url, self.justin_api = JustinApi.open_request(self.consumer_key, self.consumer_secret)
                self.justin_api.set_save_method(self.set_justin_api_persistent)
                webbrowser.open(url)
                QtGui.QMessageBox.information(self.widget,
                    "justin.tv authentication", 
                    self.gui.uiTranslator.translate('rtmp', "An authorization URL should have opened in your browser.\n" \
                        "If not, go open the following URL to allow freeseer to manage your justin.tv channel.\n" \
                        "%1").arg(url), 
                    QtGui.QMessageBox.Ok, 
                    QtGui.QMessageBox.Ok)
        except KeyError:
            logging.error("justin.tv API error: Authentication failed. Supplied credentials may be incorrect.")
            QtGui.QMessageBox.critical(self.widget, 
                "justin.tv error", 
                self.gui.uiTranslator.translate('rtmp', "Authentication failed. Supplied credentials for Justin.tv" \
                    " may be incorrect."), 
                QtGui.QMessageBox.Ok,
                QtGui.QMessageBox.Ok)
            
    def get_properties(self):
        return ['StreamURL', 'AudioQuality', 'VideoBitrate', 'VideoTune', 'AudioCodec', 'Streaming Destination']
    
    def get_property_value(self, property):
        if property == "StreamURL":
            return self.url
        elif property == "AudioQuality":
            return self.audio_quality
        elif property == "VideoBitrate":
            return self.video_bitrate
        elif property == "VideoTune":
            return self.video_tune
        elif property == "AudioCodec":
            return self.audio_codec
        else:
            return "There's no property with such name"
        
    def set_property_value(self, property, value):
        if property == "StreamURL":
            return self.set_stream_url(value)
        elif property == "AudioQuality":
            return self.set_audio_quality(value)
        elif property == "VideoBitrate":
            return self.set_video_bitrate(value)
        elif property == "VideoTune":
            return self.set_video_tune(value)
        elif property == "AudioCodec":
            return self.set_audio_codec(value)
        elif property == "Streaming Destination":
            return self.set_streaming_dest(value)
        else:
            return "Error: There's no property with such name" 

class JustinApi:
    addr = 'api.justin.tv'
    
    @staticmethod
    def open_request(consumer_key, consumer_secret):
        """
        returns request url and JustinClient object
        the object will need to obtain access token on first use
        """
        consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        url = "http://%s/oauth/request_token" % JustinApi.addr
        request = oauth.OAuthRequest.from_consumer_and_token(
            consumer,
            None,
            http_method='GET',
            http_url=url)
        
        request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, None)
        
        connection = httplib.HTTPConnection(JustinApi.addr)
        connection.request('GET', request.http_url, headers=request.to_header())
        result = connection.getresponse().read()
        
        token = oauth.OAuthToken.from_string(result)
        
        auth_request = oauth.OAuthRequest.from_token_and_callback(
            token=token,
            callback='http://localhost/',
            http_url='http://%s/oauth/authorize' % JustinApi.addr)

        return auth_request.to_url(), JustinApi(consumer_key=consumer_key, consumer_secret=consumer_secret, request_token_str=result)

    @staticmethod
    def from_string(persistent_obj):
        """
        Returns JustinClient object from string.
        """
        consumer_key, consumer_secret, request_token_str, access_token_str = pickle.loads(persistent_obj)
        return JustinApi(consumer_key, consumer_secret, request_token_str, access_token_str)

    def __init__(self, consumer_key="", consumer_secret="", request_token_str="", access_token_str=""):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.request_token_str = request_token_str
        self.access_token_str = access_token_str
        

    def set_save_method(self, save_method):
        """
        upon obtaining an access token, this object will be have a different
        serialization

        in order to support this the given save_method should be called
        upon any such change with the new serialization as its only argument
        """
        self.save_method = save_method
        self.save_method(self.to_string())

    def obtain_access_token(self):
        try:
            consumer = oauth.OAuthConsumer(self.consumer_key, self.consumer_secret)
            token = oauth.OAuthToken.from_string(self.request_token_str)
            url = "http://%s/oauth/access_token" % JustinApi.addr
            request = oauth.OAuthRequest.from_consumer_and_token(
                consumer,
                token,
                http_method='GET',
                http_url=url)
            request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, token)
            connection = httplib.HTTPConnection(self.addr)
            connection.request('GET', request.http_url, headers=request.to_header())
            result = connection.getresponse().read()
            self.access_token_str = result
            access_token = oauth.OAuthToken.from_string(result)
            self.save_method(self.to_string())
        except KeyError:
            logging.error("justin.tv API: failed to obtain an access token")

    def get_data(self, endpoint):
        try:
            token = oauth.OAuthToken.from_string(self.access_token_str)
            consumer = oauth.OAuthConsumer(self.consumer_key, self.consumer_secret)
            request = oauth.OAuthRequest.from_consumer_and_token(
                consumer,
                token,
                http_method='GET',
                http_url="http://%s/api/%s" % (JustinApi.addr, endpoint))
            request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, token)
            connection = httplib.HTTPConnection(self.addr)
            connection.request('GET', request.http_url, headers=request.to_header())
            result = connection.getresponse().read()
            data = simplejson.loads(result)
        except KeyError, simplejson.decoder.JSONDecodeError:
            logging.error("justin.tv API: failed fetch data from endpoint %s" % endpoint)
            return dict()
        return data

    def set_data(self, endpoint, payload):
        try:
            token = oauth.OAuthToken.from_string(self.access_token_str)
            consumer = oauth.OAuthConsumer(self.consumer_key, self.consumer_secret)
            request = oauth.OAuthRequest.from_consumer_and_token(
                consumer,
                token,
                http_method='POST',
                http_url="http://%s/api/%s" % (JustinApi.addr, endpoint),
                parameters=payload)
            request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, token)
            connection = httplib.HTTPConnection(self.addr)
            connection.request('POST', request.http_url, body=request.to_postdata())
            result = connection.getresponse().read()
        except KeyError:
            logging.error("justin.tv API: failed write data to endpoint %s" % endpoint)
            return None
        return result

    def set_channel_status(self, status, description):
        if not self.access_token_str:
            self.obtain_access_token()
        data = self.get_data("account/whoami.json")
        if not data:
            return
        login = data['login']
        data = self.get_data('channel/show/%s.json' % login)
        update_contents = {
            'title': status,
            'status': status,
            'description': description,
        }
        self.set_data('channel/update.json', update_contents)
    
    def to_string(self):
        return pickle.dumps([self.consumer_key, self.consumer_secret, str(self.request_token_str), str(self.access_token_str)])
