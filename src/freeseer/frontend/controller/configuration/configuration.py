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
import ConfigParser
import signal
import re

from flask import Blueprint
from flask import request

from freeseer import settings
from freeseer import logging
from freeseer.framework.plugin import PluginManager
from freeseer.framework.config.profile import ProfileDoesNotExist
from freeseer.framework.config.profile import ProfileAlreadyExists
from freeseer.frontend.controller.server import http_response
from freeseer.frontend.controller.server import HTTPError
from freeseer.frontend.controller.configuration.helpers import load_profile_configuration
from freeseer.frontend.controller.configuration.helpers import load_profile
from freeseer.frontend.controller.configuration.helpers import map_plugin_name
from freeseer.frontend.controller.configuration.helpers import get_id_from_section
from freeseer.frontend.controller.configuration.helpers import get_plugin_config
from freeseer.frontend.controller.configuration.helpers import instantiate_plugin_config
from freeseer.frontend.controller.configuration.helpers import map_plugin_category
from freeseer.frontend.controller.configuration.helpers import pack_configuration
from freeseer.frontend.controller.configuration.helpers import update_config


log = logging.getLogger(__name__)
configuration = Blueprint('configuration', __name__)


@configuration.before_app_first_request
def configure_configuration():
    """
    Runs on first call to server.
    """
    signal.signal(signal.SIGINT, teardown_configuration)


def teardown_configuration(signum, frame):
    """
    Teardown method for configuration api.
    """
    pass


@configuration.route('/profiles', methods=['GET'])
@http_response(200)
def list_profiles():
    """
    List available configuration profiles.
    """
    return {
        'profiles': settings.profile_manager.list_profiles()
    }


@configuration.route('/profiles/<string:profile>', methods=['GET'])
@http_response(200)
def view_profile(profile):
    """
    View the configuration profile specified by profile.

    Raises:
        HTTPError: If profile doesn't exist.
    """
    profile_configuration = load_profile_configuration(profile)
    return pack_configuration(profile_configuration)


@configuration.route('/profiles', methods=['POST'])
@http_response(201)
def create_profile():
    """
    Create new profile under 'name' specified in request arg.

    Raises:
        HTTPError: If profile name is invalid, or profile already exists..
    """
    pattern = '^\w+$'
    profile_name = request.form['name']
    if not re.match(pattern, profile_name):
        raise HTTPError(400, 'Invalid Profile Name: {}'.format(profile_name))

    try:
        settings.profile_manager.create(profile_name)
    except ProfileAlreadyExists:
        raise HTTPError(400, 'Profile Already Exists')
    return ''


@configuration.route('/profiles/<string:profile>', methods=['DELETE'])
@http_response(204)
def delete_profile(profile):
    """
    Delete the profile specified by profile.

    Raises:
        HTTPError: If profile doesn't exist.
    """
    try:
        settings.profile_manager.delete(profile)
    except ProfileDoesNotExist:
        HTTPError(400, 'Profile Does Not Exist')
    return ''


@configuration.route('/profiles/<string:profile>', methods=['PATCH'])
@http_response(200)
def modify_profile(profile):
    """
    Modify the profile specified by given profile name.

    Raises:
        HTTPError: If profile doesn't exist, or changes don't conform
            to Config's schema.
    """
    profile_configuration = load_profile_configuration(profile)
    changes = request.form
    update_config(profile_configuration, changes)
    return ''


@configuration.route('/profiles/<string:profile>/general', methods=['GET'])
@http_response(200)
def view_general_configuration(profile):
    """
    Returns the general configuration for the given profile.

    Raises:
        HTTPError: If profile does not exist.
    """
    profile_configuration = load_profile_configuration(profile)
    return pack_configuration(profile_configuration, include=['default_language', 'auto_hide'])


@configuration.route('/profiles/<string:profile>/general', methods=['PATCH'])
@http_response(200)
def modify_general_configuration(profile):
    """
    Modifies the general configuration for the given profile.

    Raises:
        HTTPError: If profile does not exist or changes don't conform to
            Config's schema.
    """
    profile_configuration = load_profile_configuration(profile)
    changes = request.form
    update_config(profile_configuration, changes)
    return ''


@configuration.route('/profiles/<string:profile>/recording', methods=['GET'])
@http_response(200)
def view_recording_configuration(profile):
    """
    Returns the recording configuration for the given profile.

    Raises:
        HTTPError: If profile does not exist.
    """
    profile_configuration = load_profile_configuration(profile)
    return pack_configuration(profile_configuration, include=[
        'record_to_file',
        'videodir',
        'record_to_file_plugin',
        'record_to_stream',
        'record_to_stream_plugin',
        'enable_audio_recording',
        'audiomixer',
        'enable_video_recording',
        'videomixer',
    ])


@configuration.route('/profiles/<string:profile>/recording', methods=['PATCH'])
@http_response(200)
def modify_recording_configuration(profile):
    """
    Modifies the recording configuration for the given profile.

    Raises:
        HTTPError: If profile does not exist or changes don't conform
            to Config's schema.
    """
    profile_configuration = load_profile_configuration(profile)
    changes = request.form
    update_config(profile_configuration, changes)
    return ''


@configuration.route('/profiles/<string:profile>/recording/<string:category>', methods=['GET'])
@http_response(200)
def list_plugin_category(profile, category):
    """
    List the available plugins for the given profile and plugin category.

    Raises:
        HTTPError: If profile, or category do not exist.
    """
    profile_configuration = load_profile_configuration(profile)
    plugin_manager = PluginManager(profile_configuration)
    plugin_infos = plugin_manager.get_plugins_of_category(map_plugin_category(category))
    return {
        'plugins': [plugin.name for plugin in plugin_infos]
    }


@configuration.route('/profiles/<string:profile>/recording/<string:category>/<string:plugin>', methods=['GET'])
@http_response(200)
def list_plugin_instances(profile, category, plugin):
    """
    List existing plugin instances for the given profile, plugin category,
    and plugin type.

    Raises:
        HTTPError if profile, category, or plugin don't exist.
    """
    profile_instance = load_profile(profile)
    plugin_manager = PluginManager(profile_instance)
    plugin_class = plugin_manager.get_plugin_by_name(map_plugin_name(plugin),
                                                     map_plugin_category(category))
    if not plugin_class:
        raise HTTPError(400, 'No plugin {} of type {}'.format(plugin, category))

    storage = profile_instance.get_storage('plugin.conf')
    parser = ConfigParser.ConfigParser()
    parser.read([storage._filepath])
    uids = []
    for section in parser._sections.keys():
        if plugin_class.name in section:
            uids.append(get_id_from_section(section))

    return {'instances': uids}


@configuration.route('/profiles/<string:profile>/recording/<string:category>/<string:plugin>/<string:id>', methods=['GET'])
@http_response(200)
def view_plugin_instance(profile, category, plugin, id):
    """
    View the config for instance id of the given profile, plugin category,
    and plugin type.

    Raises:
        HTTPError: If profile, category, or plugin do not exist.
    """
    plugin_config = get_plugin_config(profile, category, plugin, id)
    return pack_configuration(plugin_config)


@configuration.route('/profiles/<string:profile>/recording/<string:category>/<string:plugin>', methods=['POST'])
@http_response(200)
def create_plugin_instance(profile, category, plugin):
    """
    Create a new instance of a plugin for the given profile, plugin category,
    and plugin type.

    Raises:
        HTTPError: If profile does not exist.
    """
    uid = instantiate_plugin_config(profile, category, plugin)
    return {'id': uid}


@configuration.route('/profiles/<string:profile>/recording/<string:category>/<string:plugin>/<string:id>',
                     methods=['PATCH'])
@http_response(200)
def modify_plugin_instance(profile, category, plugin, id):
    """
    Modify the config for an instance id of the plugin for the given profile,
    and plugin category.

    Raises:
        HTTPError: If profile, category, or plugin do not exist, or if
            changes do not conform to Config's schema.

    TODO: Freeseer's PluginManager does not currently keep track of which
    instance of a plugin is being used. Instance selection is instead done
    in the widget loading code for the mixer plugins. In for a config API
    user to be able to select specific plugin instances to use in a given
    mixer, PluginManager will need to be extended to keep track of instances,
    and to write the instance id for a plugin to the plugin.conf file.
    """
    plugin_config = get_plugin_config(profile, category, plugin, id)
    changes = request.form
    update_config(plugin_config, changes)
    return ''
