'''
freeseer - vga/presentation capture software

Copyright (C) 2011-2012  Free and Open Source Software Learning Centre
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

@author: Mike Chong
'''

import ConfigParser
import httplib
import xml.etree.ElementTree as ET
import xml.sax.handler
import xml.sax

import pygst
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IOutput
from freeseer.framework.core import FreeseerCore
from freeseer.framework.presentation import Presentation

# @brief - This class manages authentication for a youtube account
# actually, I think Mitchell might have written something for this, so this is just a placeholder for now.
class YoutubeLogin(object):
	access_token = "login"
    def __init__(self, configdir):
    	pass

# @brief - This class handles api calls for
# managing Youtube Live Events

# TODO - Right now, if a user is cannot create live events, presumably, these call just fail.
# it's possible to check if the user is able to create live events, perhaps we should do that. See:
# https://developers.google.com/youtube/2.0/developers_guide_protocol_retrieving_live_events#Can_User_Create_Live_Events

class YoutubeLiveEventsManager(object):

	host = "gdata.youtube.com"
	default_user_path = "/feeds/api/users/default" # requires login authentication token - see https://developers.google.com/youtube/2.0/developers_guide_protocol_authentication#Authentication
	live_events_path = default_user_path + "/live/events"
	developer_key = "devkey" # requires a developer key - see http://code.google.com/apis/youtube/dashboard
	
	xml_encoding = "UTF-8"
	
	headers = {}
	
	ID_ATTR = "youtube_live_event_id"
	RTMP_URL_ATTR = "youtube_live_event_stream_url"
    
    def __init__(self, configdir):
    	self.login = YoutubeLogin(configdir)
    	self.headers = {"Content-type": "application/atom+xml",
    					"Authorization": "Bearer " + self.login.access_token,
    					"GData-Version": "2",
    					"X-GData-Key": "key=" + self.developer_key}
    
    # --- Event Managing Methods ---
    
    # @brief - Creates a Youtube Live Event
    # @param presentation - a Presentation for which to create
    # a live event
    
    # TODO - Include CDN information for video, or add filters based on
    # CDN response information.  *** I don't know what happens when
    # Youtube is streamed video with different CDN than it expects.
    def create_event(self, presentation):
    	entry = self.base_event_xml(presentation)
    	#TODO - Verify time format is correct
    	when = ET.SubElement(entry, "yt:when", {"start": presentation.time})
    	#TODO - add more metadata?
    	
    	resp =self.send_request("POST", ET.tostring(entry, self.xml_encoding))
    	
    	if resp.status 1= httplib.OK:
    		logging.debug("Create failed! - " resp.status + " " + resp.reason)
    	else:
    		self.handle_response(response, presentation)
    		logging.debug("Presentation Created - id=" + getattr(presentation, ID_ATTR))
    		logging.debug("RTMP Streaming URL = " + getattr(presentation, RTMP_URL_ATTR))
    
    # @brief - Updates a Youtube Live Event
    # @param presentation - A Presentation for which to create
    # a live event
    # @return - 
    def update_event(self, presentation, start=None, end=None):
    	if not hasattr(presentation, ID_ATTR):
    		logging.debug("Presentation has no id!")
    		return
    		
    	entry = self.base_event_xml(presentation)
    	entry.set("gd:fields", "title,summary,yt:when")
    	
    	if start:
    		ET.SubElement(entry, "yt:when", {"start": "now"})
    	elif end:
    		ET.SubElement(entry, "yt:when", {"end": "now"})
    	else
    		ET.SubElement(entry, "yt:when", {"start": presentation.time})
    	
    	resp = self.send_event_request("self.xml_from_presentation(presentation)",
    								   ET.tostring(entry, self.xml_encoding),
    								   getattr(presentation, ID_ATTR))
    	
    	if resp.status 1= httplib.OK:
    		logging.debug("Update failed! - " resp.status + " " + resp.reason)
    	else:
    		logging.debug("Presentation Updated - id=" + getattr(presentation, ID_ATTR))
    		logging.debug("RTMP Streaming URL = " + getattr(presentation, RTMP_URL_ATTR))
    
    # @brief - Starts a Youtube Live Event
    # @param presentation - Presentation to start
    def start_event(self, presentation):
    	self.update_event(presentation, start=True)
    
    # @brief - Ends a Youtube Live Event
    # @param presentation - Presentation to end
    def end_event(self, presentation):
    	self.update_event(presentation, end=True)
    
    # @brief - Deletes a Youtube Live Event
    # @param presentation - Presentation for live event to Delete
    # a live event
    def delete_event(self, presentation):
    	if not hasattr(presentation, ID_ATTR):
    		logging.debug("Presentation has no id!")
    		return
    	resp = self.send_event_request("DELETE", event_id=getattr(presentation, ID_ATTR))
    	if resp.status 1= httplib.OK:
    		logging.debug("Delete failed! - " resp.status + " " + resp.reason)
    	else:
    		logging.debug("Presentation Deleted - id=" + getattr(presentation, ID_ATTR))
    		delattr(presentation, ID_ATTR)
    
    # --- HTTP Request Methods ---
    
    # @brief - Sends an event request, using the appropriate headers
    # @param method - HTTP request method
    # @param body - string body to send
    # @param event_id - event id, if necessary
    # @return - the response
	# TODO - maybe reuse connections - i.e, don't open a new connection every time
    def send_event_request(self, method, body=None, event_id=None):
    	path = live_events_path
    	if event_id != None:
    		path = self.live_events_path + "/" + event_id
    	conn = httplib.HTTPConnection(self.host)
    	conn.request(method, path, body, self.headers)
    	return conn.getresponse()
    
    # @brief - Handles a Youtube Live Events API response
    # N.B. adds event id to the presentation, as well as sreaming url
    # @param response_xml - the ET object from the response
    # @param presentation - a Presentation to update
    def handle_response(self, response_xml, presentation):
    	return
    	
    # --- HTTP Request Methods ---
    
    # @brief - Handles a Youtube Live Events API response
    # @param presentation - a Presentation to use for data
    # @return - 'base' ElementTree for request body
	def base_event_xml(self, presentation)
    	entry = ET.Element("entry", {"xmlns": "http://www.w3.org/2005/Atom",
    								 "xmlns:yt": "http://gdata.youtube.com/schemas/2007"})
    	title = ET.SubElement(entry, "title")
    	title.text = presentation.title
    	summary = ET.SubElement(entry, "summary")
    	summary.text = presentation.title
    	return entry
