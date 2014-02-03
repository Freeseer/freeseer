#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
# Copyright (C) 2013 Free and Open Source Software Learning Centre
# http://fosslc.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/


import httplib
import httplib2
import logging
import os
import time

from apiclient import discovery
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from mutagen import oggvorbis
from oauth2client import file
from oauth2client import client
from oauth2client import tools

log = logging.getLogger(__name__)


class Response(object):
    """Class to serve as enum for responses"""

    SUCCESS = 0
    UNEXPECTED_FAILURE = 1
    UNRETRIABLE_ERROR = 2
    ACCESS_TOKEN_ERROR = 3
    MAX_RETRIES_REACHED = 4


class YoutubeService(object):
    """Class for interacting with YouTube Data API v3"""

    # Status codes and exceptions for retry logic
    MAX_RETRIES = 3
    RETRIABLE_EXCEPTIONS = (
        httplib2.HttpLib2Error,
        IOError,
        httplib.NotConnected,
        httplib.IncompleteRead,
        httplib.ImproperConnectionState,
        httplib.CannotSendRequest,
        httplib.CannotSendHeader,
        httplib.ResponseNotReady,
        httplib.BadStatusLine
    )
    RETRIABLE_STATUS_CODES = (500, 502, 503, 504)

    def __init__(self):
        """Initialize YoutubeService setting up http related values"""
        # Tell the underlying HTTP transport library not to retry, we want explicit control over the retry logic
        # and to only retry on errors/exceptions specified by Google
        httplib2.RETRIES = 1

    def authenticate(self, client_secrets, oauth2_token, flags):
        """Handles the authentication process using OAuth2 protocol

        Args:
            client_secrets: path to client_secrets file
            oauth2_token: path to oauth2_token to use, if none present token will be saved here
            flags: flags to pass to Google Python Client's argparser
        """
        scope = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube']
        message = ("Please specify a valid client_secrets.json file.\n"
                    "To obtain one, please visit:\n"
                    "https://docs.google.com/document/d/1ro9I8jnOCgQlWRRVCPbrNnQ5-bMvQxDVg6o45zxud4c/edit")
        storage = file.Storage(oauth2_token)
        flow = client.flow_from_clientsecrets(client_secrets, scope=scope, message=message)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(flow, storage, flags)
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('youtube', 'v3', http=http)

    def insert_broadcast(self):
        """Function to create a broadcast for livestreaming"""
        part = "snippet,status"
        body = {
            "kind" : "youtube#liveBroadcast",
            "snippet" : {
                "title" : "",
                "scheduledStartTime" : "",
                "scheduledEndTime" : ""
            } 
        }
        status = {
            "privacyStatus" : ""
        }
        response = self.service.liveBroadcast().insert(part=part,body=body,status=status).execute()

    def upload_video(self, video_file):
        """Function to upload file to Youtube

        Function grabs metadata from video_file and passes it along in the upload, the files privacy and license are
        set to public and youtube respectively

        Args:
            video_file: path to video file for upload

        Returns:
            a tuple containing a response code and a dictionary with the appropriate information
        """
        part = "snippet,status"
        metadata = self.get_metadata(video_file)
        body = {
            "snippet": {
                "title": metadata['title'],
                "description": metadata['description'],
                "tags": metadata['categoryId'],
                "categoryId": metadata['categoryId']
            },
            "status": {
                "privacyStatus": "public",
                "license": "youtube",   # temporary, see gh#414
                "embeddable": True,
                "publicStatsViewable": True
            }
        }
        # this is to fix a bug, the API thinks our .ogg files are audio/ogg
        mimetype = "video/{}".format(video_file.split(".")[-1])
        media_body = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype=mimetype)
        insert_request = self.service.videos().insert(part=part, body=body, media_body=media_body)
        response = None
        error = None
        retry = 0
        sleep_seconds = 5.0
        while response is None:
            try:
                log.info("Uploading %s" % video_file)
                (status, response) = insert_request.next_chunk()
                if 'id' in response:
                    return (Response.SUCCESS, response)
                else:
                    return (Response.UNEXPECTED_FAILURE, response)
            except HttpError as e:
                if e.resp.status in self.RETRIABLE_STATUS_CODES:
                    error = "A retriable HTTP error {} occurred:\n{}".format(e.resp.status, e.content)
                else:
                    return (Response.UNRETRIABLE_ERROR, {"status": e.resp.status, "content": e.content})
            except self.RETRIABLE_EXCEPTIONS as e:
                error = "A retriable error occurred: {}".format(e)
            except client.AccessTokenRefreshError:
                return (Response.ACCESS_TOKEN_ERROR, None)
            if error is not None:
                log.error(error)
                retry += 1
                if retry > self.MAX_RETRIES:
                    return (Response.MAX_RETRIES_REACHED, None)
                log.info("Sleeping %s seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

    def valid_video_file(self, file):
        """Verify file is supported by Youtube

        Freeseer currently encodes to .ogg and .webm
        TODO: expand list to all types supported by Youtube

        Args:
            file: path to file to verify

        Returns:
            True if file is supported
        """
        return file.lower().endswith(('.ogg', '.webm'))

    def get_metadata(self, video_file):
        """Parses file metadata

        Parsing is delegated to appropriate library based on filetype
        If filetype is unsupported default metadata is used instead

        Args:
            video_file: path to file

        Returns:
            Metadata formatted to Youtube APIs status parameter
        """
        metadata = {
            "title": os.path.basename(video_file).split(".")[0],
            "description": "A video recorded with Freeseer",
            "tags": ['Freeseer', 'FOSSLC', 'Open Source'],
            "categoryId": 27    # temporary, see gh#415
        }
        if video_file.lower().endswith('.ogg'):
            tags = oggvorbis.Open(video_file)
            if "title" in tags:
                metadata['title'] = tags['title'][0]
            if "album" in tags and "artist" in tags and "date" in tags:
                metadata['description'] = "At {} by {} recorded on {}".format(tags['album'][0], tags['artist'][0], tags['date'][0])
        return metadata
