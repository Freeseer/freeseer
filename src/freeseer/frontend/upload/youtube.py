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


import argparse
import ConfigParser
import os

from oauth2client import tools

from freeseer.framework.youtube import Response
from freeseer.framework.youtube import YoutubeService
from freeseer.settings import configdir


class YoutubeFrontend(object):
    """Frontend class of Youtube Framework

    Class currently only features command line support
    """

    def __init__(self):
        """Constructor for YoutubeFrontend

        Initializes parser inherited from Google Python Client
        Also sets default folders and filepaths
        """
        self.parser = argparse.ArgumentParser(
            description="Youtube Framework",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[tools.argparser])
        self.set_defaults()

    def set_defaults(self):
        """Set the path for the default video folder, client_secrets, and oauth2_token"""
        config = ConfigParser.ConfigParser()
        configfile = os.path.join(configdir, "freeseer.conf")
        config.readfp(open(configfile))
        self.video_directory = config.get('Global', 'video_directory')
        self.client_secrets = os.path.join(configdir, "client_secrets.json")
        self.oauth2_token = os.path.join(configdir, "oauth2_token.json")

    def cmd_line(self, argv):
        """Initializes command line interface

        Args:
            argv: command line arguments to parse
        """
        self.parser.add_argument("-c", "--client_secrets",
                                 help="Path to client secrets file", default=self.client_secrets)
        self.parser.add_argument("-t", "--token",
                                 help="Path to OAuth2 token", default=self.oauth2_token)
        self.parser.add_argument("-f", "--files",
                                 help="Path to file or filefolder for upload", default=self.video_directory)
        self.parser.add_argument("-y", "--yes",
                                 help="Assume yes", action="store_true")
        flags = self.parser.parse_args(argv[1:])
        youtube_service = YoutubeService()
        # command line arguments neede for Google Python Client need to always be passed in for authentication
        youtube_service.authenticate(flags.client_secrets, flags.token, flags)
        # path doesn't exist, print an error message
        if not os.path.exists(flags.files):
            print "{} does not exit".format(flags.files)
        # path is a folder, upload all videos in the folder
        elif os.path.isdir(flags.files):
            self.upload_folder_cmd_line(youtube_service, flags.files, flags.yes)
        # single file check if it is an uploadable video file
        elif youtube_service.valid_video_file(flags.files):
            if flags.yes:
                self.handle_response(youtube_service.upload_video(flags.files))
            else:
                response = raw_input(
                    "Are you sure you would like to upload the following file? [Y/n]\n" + flags.files + "\n")
                if response.lower() in ('', 'y', 'yes'):
                    self.handle_response(youtube_service.upload_video(flags.files))
        # if this case is reached it means there is nothing to upload
        else:
            print "Nothing to upload"

    def upload_folder_cmd_line(self, youtube_service, folder, assume_yes):
        """For uploading an entire folder of videos to Youtube"""
        # these vars are for confirmation purposes
        files_to_upload = []
        list_files_msg = ""
        # walk through the folder
        for root, dirs, files in os.walk(folder):
            # foreach file (we aren't crawling through subfolders)
            for file in files:
                filepath = os.path.join(root, file)
                # if the file is a video file mark it for upload
                if youtube_service.valid_video_file(filepath):
                    # if --yes was passed, do not prompt just upload
                    if assume_yes:
                        print youtube_service.upload_video(filepath)
                        # otherwise build a message and add the file to the to_upload list
                    else:
                        files_to_upload.append(filepath)
                        list_files_msg += "{}\n".format(filepath)
        # this var will only be populated if --yes was NOT passed as an argument
        # by the user, therefore the list of files to be uploaded will be printed
        # and confirmation is asked
        if files_to_upload:
            response = raw_input(
                "Are you sure you would like to upload the following files? [Y/n]\n%s" % list_files_msg)
            if response.lower() in ('', 'y', 'yes'):
                for file in files_to_upload:
                    self.handle_response(youtube_service.upload_video(file))

    def handle_response(self, (response_code, response)):
        """Process the response from the Youtube API"""
        if response_code is Response.SUCCESS:
            print "The file was successfully uploaded with video id: {}".format(response['id'])
        elif response_code is Response.UNEXPECTED_FAILURE:
            print "The file failed to upload with unexpected response: {}".format(response)
        elif response_code is Response.UNRETRIABLE_ERROR:
            print "An unretriable HTTP error {} occurred:\n{}".format(respnse['status'], response['content'])
        elif response_code is Response.MAX_RETRIES_REACHED:
            print "The maximum number of retries has been reached"
        elif response_code is Response.ACCESS_TOKEN_ERROR:
            print "The access token has expired or been revoked, please run .authenticate()"
