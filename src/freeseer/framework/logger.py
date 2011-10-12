#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2011  Free and Open Source Software Learning Centre
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
# http://wiki.github.com/fosslc/freeseer/

import ConfigParser
import logging
import logging.config
import os
import sys
import socket
from logging.handlers import SYSLOG_TCP_PORT

class Logger():
    '''
    This class is responsible for initializing the logger and reading/writing
    settings to the logging.conf file.
    '''

    def __init__(self, configdir):
        '''
        Initialize settings from a configfile
        '''
        self.configdir = configdir
        self.logconf = os.path.abspath("%s/logging.conf" % self.configdir)
        
        # If logger.conf does not exist then create it with some defaults.
        if not os.path.isfile(self.logconf):
            self.writeConfig()
            
        try:
            logging.config.fileConfig(self.logconf)
            logging.info('Logger initialized.')
        except socket.error:
            sys.stderr.write('Logger failed to initialize\n')
        
    def writeConfig(self):
        '''
        This function creates / saves log settings to a file.
        '''
        config = ConfigParser.ConfigParser()
        config.add_section('loggers')
        config.set('loggers', 'keys', 'root')
        
        config.add_section('formatters')
        config.set('formatters', 'keys', 'basic,nix')
        
        config.add_section('handlers')
        config.set('handlers', 'keys', 'consoleHandler,syslogHandler')
        
        config.add_section('logger_root')
        config.set('logger_root', 'level', 'DEBUG')
        config.set('logger_root', 'handlers', 'consoleHandler,syslogHandler')
        
        config.add_section('handler_consoleHandler')
        config.set('handler_consoleHandler', 'class', 'StreamHandler')
        config.set('handler_consoleHandler', 'level', 'NOTSET')
        config.set('handler_consoleHandler', 'formatter', 'basic')
        config.set('handler_consoleHandler', 'args', '(sys.stdout,)')
        
        config.add_section('handler_syslogHandler')
        config.set('handler_syslogHandler', 'level', 'NOTSET')
        if sys.platform.startswith('linux'):
            config.set('handler_syslogHandler', 'class', 'handlers.SysLogHandler')
            config.set('handler_syslogHandler', 'formatter', 'nix')
            config.set('handler_syslogHandler', 'args', "("+self.getLogPath()+", handlers.SysLogHandler.LOG_USER)")
        elif sys.platform == 'win32' or sys.platform == 'cygwin':
            config.set('handler_syslogHandler', 'class', 'handlers.NTEventLogHandler')
            config.set('handler_syslogHandler', 'formatter', 'nix')
            config.set('handler_syslogHandler', 'args', "('Freeseer', '', 'Application')")
        elif sys.platform =='darwin':
            config.set('handler_syslogHandler', 'class', 'handlers.SysLogHandler')
            config.set('handler_syslogHandler', 'formatter', 'nix')
            config.set('handler_syslogHandler', 'args', "("+self.getLogPath()+", handlers.SysLogHandler.LOG_USER)")
            #config.set('handler_syslogHandler', 'args', "(('/dev/log'), handlers.SysLogHandler.LOG_USER)")
        else:
            pass # Unsupported
        
        config.add_section('formatter_basic')
        config.set('formatter_basic', 'format', '%(asctime)s freeseer: <%(levelname)s> %(message)s')
        config.set('formatter_basic', 'datefmt', '%Y-%m-%d %H:%M:%S')
        
        config.add_section('formatter_nix')
        config.set('formatter_nix', 'format', 'freeseer: <%(levelname)s> %(message)s')
        
        # Save default settings to new config file
        with open(self.logconf, 'w') as configfile:
            config.write(configfile)

    def getLogPath(self):
        logPath = ['/dev/log', '/var/run/syslog']
        for x in logPath:
            ## Test UDP connection
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            try:
                self.socket.connect(x)
                return "'"+x+"'"
            except socket.error:
                self.socket.close()
                
            ## Test TCP connection
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                self.socket.connect(x)
                return "'"+x+"'"
            except socket.error:
                self.socket.close()
        ## Default back to localhost        
        return "('localhost', handlers.SYSLOG_UDP_PORT)"
        
if __name__ == "__main__":
    logger = Logger(os.path.abspath(os.path.expanduser('~/.freeseer/')))
    logger.log.debug('This is a debug log')
    logger.log.critical('This is a critical log')
    logger.log.error('This is an error log')
    logger.log.info('This is an info log')
    logger.log.warning('This is a warning log')
