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


import os

from freeseer import settings
from freeseer.framework.youtube import Response
from freeseer.framework.youtube import YoutubeService


class YoutubeFrontend(object):
    """Frontend class of Youtube Framework

    Class currently only features command line support
    """

    @staticmethod
    def get_defaults():
        """Retrieve the defaults value for client_secrets, video folder, etc.

        Returns:
            dictionary of default values which are:
            client_secrets: ~/<configdir>/client_secrets.json
            oauth2_token: ~/<configdir>/oauth2_token.json
            video_directory: ~/Videos
        """
        profile = settings.profile_manager.get("default")
        config = profile.get_config('freeseer.conf', settings.FreeseerConfig, storage_args=['Global'], read_only=True)
        return {
            "video_directory": config.videodir,
            "oauth2_token": os.path.join(settings.configdir, "oauth2_token.json"),
            "client_secrets": os.path.join(settings.configdir, "client_secrets.json")
        }

    def upload(self, files, token, yes):
        """Uploads a file(s) to YouTube using the YouTube service API

        This function uploads a list of videos and/or directories of videos to YouTube.

        Args:
            token            - location of an oauth2 token
            files            - list of files and directories to upload
            yes              - if True, assume yes to all interaction (default: False)
        """
        # check if token exists
        if not os.path.exists(token):
            print("{} does not exist, please specify a valid token file".format(token))
            return
        # gather videos specified and vids from folders specified into list
        videos = []
        for item in files:
            # crawl subfolders
            if os.path.isdir(item):
                for root, dirs, files_ in os.walk(item):
                    for f in files_:
                        filepath = os.path.join(root, f)
                        # check if its a video and make sure its not a duplicate
                        if YoutubeService.valid_video_file(filepath) and filepath not in videos:
                            videos.append(filepath)
            # if it exists it is a single file, check if its a video, and make sure its not a duplicate
            elif os.path.exists(item) and YoutubeService.valid_video_file(item) and item not in videos:
                videos.append(item)
        # now begin upload process
        if not videos:
            print("Nothing to upload")
        else:
            youtube_service = YoutubeService()
            # authorize with OAuth2 token
            youtube_service.authorize(token)
            if not yes:
                print("Found videos:")
                print("\n".join(videos))
            question = "Are you sure you would like to upload these videos? [Y/n] "
            if yes or raw_input(question).lower() in ('', 'y', 'yes'):
                for video in videos:
                    self.handle_response(youtube_service.upload_video(video))

    def handle_response(self, (response_code, response)):
        """Process the response from the Youtube API"""
        if response_code is Response.SUCCESS:
            print("The file was successfully uploaded with video id: {}".format(response['id']))
        elif response_code is Response.UNEXPECTED_FAILURE:
            print("The file failed to upload with unexpected response: {}".format(response))
        elif response_code is Response.UNRETRIABLE_ERROR:
            print("An unretriable HTTP error {} occurred:\n{}".format(response['status'], response['content']))
        elif response_code is Response.MAX_RETRIES_REACHED:
            print("The maximum number of retries has been reached")
        elif response_code is Response.ACCESS_TOKEN_ERROR:
            print("The access token has expired or been revoked, please run python -m freeseer config youtube")
