#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2014  Free and Open Source Software Learning Centre
#  http://fosslc.org
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

# For support, questions, suggestions or any other inquiries, visit:
# http://wiki.github.com/Freeseer/freeseer/

import functools

from flask import jsonify

from freeseer.frontend.controller import app


def start_server(storage_file):
    """Starts the restapi server.

    Args:
        storage_file - name of storage file to which you are saving recordings
    """

    app.storage_file_path = storage_file
    app.run()


def http_response(status_code):
    """Wraps any function that returns a dict, converts to JSON and returns an HTTP response.

    Args:
        status_code - the http status code you want your http response to return
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                response_dict = func(*args, **kwargs)
                response = jsonify(response_dict)
                response.status_code = status_code
                return response
            except HTTPError as e:
                response = jsonify({
                    'error_message': e.message,
                    'error_code': e.status_code
                })
                response.status_code = e.status_code
                return response
        return wrapper
    return decorator


class HTTPError(Exception):

    def __init__(self, message, status_code):
        super(HTTPError, self).__init__(message)
        self.message = message
        self.status_code = status_code


class ServerError(Exception):

    def __init__(self, message):
        super(ServerError, self).__init__(message)
