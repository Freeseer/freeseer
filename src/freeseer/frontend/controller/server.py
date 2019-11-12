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
import signal
import sys

from flask import jsonify

from freeseer.frontend.controller import app
from freeseer.framework.announcer import ServiceAnnouncer


def start_server(storage_file, port=7079):
    """Starts the restapi server.

    Args:
        storage_file - name of storage file to which you are saving recordings
        port - the port you wish to broadcast your server on.
    """

    app.storage_file_path = storage_file
    app.service_announcer = ServiceAnnouncer('Freeseer Host', '_freeseer._tcp', port, [])
    app.service_announcer.advertise()
    signal.signal(signal.SIGTERM, remove)
    app.run('::0.0.0.0', port)


def remove(signal, frame):
    app.service_announcer.remove_service()
    sys.exit(0)


def http_response(status_code):
    """Wraps any function that returns a dict, converts to JSON and returns an HTTP response.

    Args:
        status_code - the http status code you want your http response to return when successful
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
                error_dict = {
                    'error_code': e.status_code,
                    'error_message': e.message,
                }
                if e.description:
                    error_dict['description'] = e.description
                response = jsonify(error_dict)
                response.status_code = e.status_code
                return response
        return wrapper
    return decorator


class HTTPError(Exception):

    HTTP_ERROR_MESSAGES = {
        400: 'Bad Request: Request could not be understood due to malformed syntax.',
        401: 'Unauthorized: Authentication was not provided or has failed.',
        404: 'Not Found: Requested resource is not available.',
        409: 'Conflict: Request could not be processed because of server conflict.',
        422: 'Unprocessable Entity: Request could not be processed due to semantic errors.',
    }

    def __init__(self, status_code, description=None):
        message = self.HTTP_ERROR_MESSAGES[status_code]
        super(HTTPError, self).__init__(message)
        self.description = description
        self.status_code = status_code


class ServerError(Exception):

    def __init__(self, message):
        super(ServerError, self).__init__(message)
