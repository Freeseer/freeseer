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
import uuid
from freeseer import settings

from freeseer.framework.config.exceptions import InvalidOptionValueError
from freeseer.framework.config.profile import ProfileDoesNotExist
from freeseer.framework.plugin import PluginManager
from freeseer.frontend.controller.server import HTTPError

plugin_types_map = {
    'audioinput': 'AudioInput',
    'audiomixer': 'AudioMixer',
    'videoinput': 'VideoInput',
    'videomixer': 'VideoMixer',
    'importer': 'Importer',
    'output': 'Output',
}

plugin_names_map = dict([(plugin.name.lower().replace(' ', ''), plugin.name)
                         for plugin in PluginManager('default').get_all_plugins()])


def map_plugin_name(plugin):
    """
    Maps a resource name to a plugin name.

    Raises:
        HTTPError: If no plugin exists by given name.
    """
    try:
        name = plugin_names_map[plugin]
    except KeyError:
        raise HTTPError(400, 'Invalid Plugin Name: {}'.format(plugin))
    return name


def map_plugin_category(category):
    """
    Maps a plugin category resource name to a plugin category name.

    Raises:
        HTTPError: If no plugin category exists by given name.
    """
    try:
        category = plugin_types_map[category]
    except KeyError:
        raise HTTPError(400, 'Invalid Plugin Category: {}'.format(category))
    return category


def update_config(config, data):
    """
    Updates given config instance with request data.

    Args:
        config: A Configuration instance.
        data: A key, value dict containing changes to config.

    Raises:
        HTTPError: If given data changes don't conform to config's schema.
    """

    for key, value in data.items():
        try:
            opt_instance = config.options[key]
            value = opt_instance.decode(value)
            setattr(config, key, value)
        except KeyError:
            raise HTTPError(400, 'Invalid Option: {}'.format(key))
        except InvalidOptionValueError:
            raise HTTPError(400, 'Invalid Value {} for option {}'.format(value, key))
    config.save()


def pack_configuration(config, include=[]):
    """
    Returns a response for the given config.

    Args:
        config: A Config instance.
        include: An optional list of Config options to include in response.

    Returns:
        A dict containing the given configuration, and its schema. If an
        'include' list is given, only the options listed are returned in
        the configuration.
    """
    conf = {}
    schema = {}

    if include:
        for key in include:
            option = config.options[key]
            conf[key] = option.presentation(config.values[key])
            schema[key] = option.schema()
    else:
        conf = config.values
        schema = config.schema()

    return {
        'configuration': conf,
        'schema': schema,
    }


def load_profile_configuration(profile):
    """
    Returns the configuration for a given profile.

    Raises:
        HTTPError: If profile does not exist.
    """
    profile_instance = load_profile(profile)
    return profile_instance.get_config('freeseer.conf', settings.FreeseerConfig, storage_args=['Global'],
                                       read_only=False)


def load_profile(profile):
    """
    Returns the profile instance for a given profile name.

    Raises:
        HTTPError: If profile does not exist.
    """
    try:
        profile = settings.profile_manager.get(profile, create_if_needed=False)
    except ProfileDoesNotExist:
        raise HTTPError(404, 'Profile Does Not Exist')
    return profile


def get_plugin_config(profile, category, plugin, id):
    """
    Returns the config instance for the given id, plugin, category, and profile.

    Args:
        profile: Name of a freeseer profile.
        category: Resource name for a category plugin.
        plugin: Resource name for a plugin type.
        id: The instance number for a plugin.

    Raises:
        HTTPError: If profile, category, or plugin don't exist.
    """
    profile_instance = load_profile(profile)
    plugin_manager = PluginManager(profile_instance)
    plugin_class = plugin_manager.get_plugin_by_name(map_plugin_name(plugin),
                                                     map_plugin_category(category))
    if not plugin_class:
        raise HTTPError(400, 'No plugin {} of type {}'.format(plugin, category))

    plugin_object = plugin_class.plugin_object
    plugin_class.plugin_object.set_instance(id)
    return plugin_object.config


def get_id_from_section(section):
    """
    Returns the uid of a plugin instance from its config section name.

    ie:
    VideoMixer Plugin: Video Passthrough-0
                                        => 0
    VideoMixer Plugin: Video Passthrough-98659d08-2eb3-4ead-96a4-53c27965ce11
                                        => 98659d08-2eb3-4ead-96a4-53c27965ce11
    """
    s = section.split('-')  # All sections guaranteed to have at least one '-' separator
    return '-'.join(s[1:])  # The uid is all of the sections after the initial '-'


def instantiate_plugin_config(profile, category, plugin):
    """
    Creates a configuration file entry for a plugin of
    the given category and type, for the given profile.

    Returns: A uid for the plugin config.
    """
    uid = uuid.uuid4()
    plugin_config = get_plugin_config(profile, category, plugin, uid)
    plugin_config.save()
    return uid
