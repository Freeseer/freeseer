#!/usr/bin/env python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2013  Free and Open Source Software Learning Centre
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


import argparse
import signal
import sys
import textwrap

import pygst
import yapsy
from PyQt4 import QtCore

from freeseer import __version__
from freeseer import settings


signal.signal(signal.SIGINT, signal.SIG_DFL)


def setup_parser():
    """Initialize the Argument Parser"""
    parser = argparse.ArgumentParser(description='Freeseer Recording Utility',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-v", "--version", action='version',
                                           version=textwrap.dedent('''\
                                           Freeseer {version} ({platform})
                                           Python {pymajor}.{pyminor}.{pymicro}
                                           PyGst {pygst_version}
                                           PyQt {pyqt_version}
                                           Qt {qt_version}
                                           Yapsy {yapsy_version}
                                           '''.format(version=__version__,
                                                      platform=sys.platform,
                                                      pymajor=sys.version_info.major,
                                                      pyminor=sys.version_info.minor,
                                                      pymicro=sys.version_info.micro,
                                                      pygst_version=pygst._pygst_version,
                                                      pyqt_version=QtCore.PYQT_VERSION_STR,
                                                      qt_version=QtCore.QT_VERSION_STR,
                                                      yapsy_version=yapsy.__version__)))

    # Configure Subparsers
    subparsers = parser.add_subparsers(dest='app', help='Command List')
    setup_parser_record(subparsers)
    setup_parser_config(subparsers)
    setup_parser_talk(subparsers)
    setup_parser_report(subparsers)
    return parser


def setup_parser_record(subparsers):
    """Setup the record command parser"""
    parser = subparsers.add_parser('record', help='Freeseer recording functions')
    parser.add_argument("-t", "--talk", type=int, help="Talk ID of the talk you would like to record")
    parser.add_argument("-f", "--filename", type=unicode, help="Record to filename")
    parser.add_argument("-p", "--profile", type=unicode, help="Use profile")
    parser.add_argument("-s", "--show-talks", help="Shows all talks", action="store_true")


def setup_parser_config(subparsers):
    """Setup the config command parser"""
    parser = subparsers.add_parser('config', help='Freeseer configuration functions')
    parser.add_argument("--reset", help="Reset's Freeseer (removes the Freeseer configuration directory)",
        action="store_true")
    parser.add_argument("--reset-configuration", help="Reset's Freeseer configuration (removes freeseer.conf and plugins.conf)", action="store_true")
    parser.add_argument("--reset-database", help="Reset's Freeseer database (removes presentations.db)", action="store_true")


def setup_parser_talk(subparsers):
    """Setup the talk command parser"""
    parser = subparsers.add_parser('talk', help='Freeseer talk database functions')
    parser.add_argument("action", choices=['add', 'remove', 'clear'], nargs='?')
    parser.add_argument("-t", "--title", type=unicode, help="Title")
    parser.add_argument("-s", "--speaker", type=unicode, help="Speaker")
    parser.add_argument("-r", "--room", type=unicode, help="Room")
    parser.add_argument("-e", "--event", type=unicode, help="Event")
    parser.add_argument("-i", "--talk-id", type=int, help="Talk ID")


def setup_parser_report(subparsers):
    """Setup the report command parser"""
    subparsers.add_parser('report', help='Freeseer reporting functions')


def parse_args(parser, parse_args=None):
    if len(sys.argv) == 1:  # No arguments passed
        launch_recordapp()

    args = parser.parse_args(parse_args)

    if args.app == 'record':
        if len(sys.argv) == 2:  # No 'record' arguments passed
            launch_recordapp()

        import gobject
        # Must declare after argparse otherwise GStreamer will take over the cli help
        from freeseer.frontend.record.RecordingController import RecordingController

        # TODO: Abstract the database stuff away from here as it's only
        #       used in conjunction with talks.
        if args.profile is None:  # Profile is an optional parameter
            args.profile = 'default'
        profile = settings.profile_manager.get(args.profile)
        config = profile.get_config('freeseer.conf', settings.FreeseerConfig,
                                    storage_args=['Global'], read_only=False)
        # XXX: There should only be 1 database per user. Workaround for this
        #      is to put it in the 'default' profile.
        db = settings.profile_manager.get().get_database()

        app = RecordingController(profile, db, config, cli=True)

        if args.talk:
            if app.record_talk_id(args.talk):
                sys.exit(gobject.MainLoop().run())
        elif args.filename:
            if app.record_filename(args.filename):
                sys.exit(gobject.MainLoop().run())
        elif args.show_talks:
            app.print_talks()

    elif args.app == 'config':
        if len(sys.argv) == 2:  # No 'config' arguments passed
            launch_configtool()

        from freeseer.settings import configdir
        from freeseer.framework.util import reset
        from freeseer.framework.util import reset_configuration
        from freeseer.framework.util import reset_database

        if args.reset:
            reset(configdir)
        elif args.reset_configuration:
            reset_configuration(configdir)
        elif args.reset_database:
            reset_database(configdir)

    elif args.app == 'talk':
        if len(sys.argv) == 2:  # No 'talk' arguments passed
            launch_talkeditor()

        from freeseer.framework.presentation import Presentation

        profile = settings.profile_manager.get()
        db = profile.get_database()

        if args.action == "add":
            presentation = Presentation(args.title,
                                        speaker=args.speaker,
                                        room=args.room,
                                        event=args.event)
            db.insert_presentation(presentation)

        elif args.action == "remove":
            db.delete_presentation(args.talk_id)

        elif args.action == "clear":
            db.clear_database()

        else:
            print("Invalid option.")

    elif args.app == 'report':
        if len(sys.argv) == 2:  # No 'report' arguments passed
            launch_reporteditor()


def launch_recordapp():
    """Launch the Recording GUI if no arguments are passed"""
    from PyQt4.QtGui import QApplication
    from freeseer.frontend.record.record import RecordApp

    profile = settings.profile_manager.get()
    config = profile.get_config('freeseer.conf', settings.FreeseerConfig,
                                storage_args=['Global'], read_only=False)

    app = QApplication(sys.argv)
    main = RecordApp(profile, config)
    main.show()
    sys.exit(app.exec_())


def launch_configtool():
    """Launch Freeseer Configuration GUI if no arguments are passed"""
    from PyQt4 import QtGui
    from freeseer.frontend.configtool.configtool import ConfigToolApp

    profile = settings.profile_manager.get()
    config = profile.get_config('freeseer.conf', settings.FreeseerConfig,
                                storage_args=['Global'], read_only=False)

    app = QtGui.QApplication(sys.argv)
    main = ConfigToolApp(profile, config)
    main.show()
    sys.exit(app.exec_())


def launch_talkeditor():
    """Launch the Talk Editor GUI if no arguments are passed"""
    from PyQt4.QtGui import QApplication
    from freeseer.frontend.talkeditor.talkeditor import TalkEditorApp

    profile = settings.profile_manager.get()
    config = profile.get_config('freeseer.conf', settings.FreeseerConfig,
                                storage_args=['Global'], read_only=True)
    db = profile.get_database()

    app = QApplication(sys.argv)
    main = TalkEditorApp(config, db)
    main.show()
    sys.exit(app.exec_())


def launch_reporteditor():
    """Launch the Report Editor GUI"""
    import sys
    from PyQt4 import QtGui
    from freeseer.frontend.reporteditor.reporteditor import ReportEditorApp

    profile = settings.profile_manager.get()
    config = profile.get_config('freeseer.conf', settings.FreeseerConfig,
                                storage_args=['Global'], read_only=True)
    db = profile.get_database()

    app = QtGui.QApplication(sys.argv)
    main = ReportEditorApp(config, db)
    main.show()
    sys.exit(app.exec_())
