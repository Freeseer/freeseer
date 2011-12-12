#!/usr/bin/python
# -*- coding: utf-8 -*-

# freeseer - vga/presentation capture software
#
#  Copyright (C) 2010  Free and Open Source Software Learning Centre
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

# pylint: disable=E1101

from twisted.conch.ssh import transport, userauth, connection, channel, keys, common, filetransfer
from twisted.internet import defer, protocol, reactor
from twisted.python import log, failure
from twisted.python.log import logging
from twisted.conch import error
import sys
import os
import getpass
import mimetypes
import base64
import xmlrpclib
import time
import gobject
gobject.threads_init() #@UndefinedVariable
import pygst
pygst.require('0.10')
import gst
from gst.extend.discoverer import Discoverer

USER = None
PASS = None
HOST = None
SRC = 'new-file'
DST = '.'
PROTOCOL = 'sftp'
EXCODE = 1
VIDEO = None

#This class handles the encryption details with the server
class Transport(transport.SSHClientTransport):
    
    #Checks to see that the fingerprint key match's up with the server's
    def verifyHostKey(self, hostKey, fingerprint):
        print ('verifyHostKey')
        return defer.succeed(1)

    #Once secure create a new connection with the user's authentication
    def connectionSecure(self):
        print ('connectionSecure')
        self.requestService(UserAuth(USER, ClientConnection()))
        
    #Stops the connection   
    def connectionLost(self, reason):
        print ('connectionLost')
#        reactor.stop()


#This class handles the SSH Authentication with either ssh keys or a user input password
class UserAuth(userauth.SSHUserAuthClient):
    
    def getPassword(self):
        print "getpassword"
        try:
            passwd = defer.succeed(getpass.getpass("%s@%s's password: " % (USER, HOST)))
        except getpass.GetPassWarning:
            print "Ooop that was not a valid password, %s" % passwd
        print "getpassword return"
        return passwd
            
    def getPublicKey(self):
#        path = os.path.expanduser('~/.ssh/id_rsa') 
#        if not os.path.exists(path) or self.lastPublicKey:
            #if the file doesn't exist, or we've tried a public key
        return
#        return keys.Key.fromFile(filename=path+'.pub').blob()

    def getPrivateKey(self):
#        path = os.path.expanduser('~/.ssh/id_rsa')
        return #defer.succeed(keys.Key.fromFile(path).keyObject)

#This class opens the connection channels
class ClientConnection(connection.SSHConnection):

    def serviceStarted(self):
        print "clientconnection servicestarted", PROTOCOL
        if PROTOCOL == 'scp':
            self.openChannel(ScpChannel(2**16, 2**15, self))
        else:
            self.openChannel(SftpChannel(2**16, 2**15, self))
#        self.openChannel(ScpChannel(2**16, 2**15, self))

#This class sets up a channel to be used by the SCPchannel
class TransferChannelBase(channel.SSHChannel):
    
    name = 'session'
    state = None
    todo = 0
    buffer = ''
        
    def channelOpen(self, data):
        # Might display/process welcome screen
        self.welcome = data
        if PROTOCOL == 'scp':
            type = 'exec'
        else:
            type = 'subsystem'
        # Call the handler
        d = self.conn.sendRequest(self, type, common.NS(PROTOCOL), wantReply=1)
        d.addCallbacks(self.channelOpened, log.err)
        
    def closed(self):
        self.loseConnection()
        reactor.stop() #@UndefinedVariable

#This class handles transferring via SCP
class ScpChannel(TransferChannelBase):
    #start SCP transfer
    def channelOpened(self, data):
        print ('scpChannelOpened')
        self.write('\0')
        self.state = 'waiting'

    def dataReceived(self, data):
        print ('dateReceived')
        # What we do with the data depends on where we are
        if self.state=='waiting':
            # we've started the transfer, and are expecting response
            # might not get it all at once, buffer
            self.buffer += data
            if not self.buffer.endswith('\n'):
                return
            b = self.buffer
            self.buffer = ''

            if not b.startswith('C'):
                self.loseConnection()
                return

            # Get the file info
            p, l, n = b[1:-1].split(' ')
            perms = int(p, 8)
            self.todo = int(l)
            
            #move onto sending the content
            self.state = 'receiving'
            self.write('\0')
            
        elif self.state=='receiving':
            
            if len(data)>self.todo:
                extra = data[self.todo:]
                data = data[:self.todo]
                
            DST.write(data)
            self.todo -= len(data)
            
            if self.todo<=0:
                self.loseConnection()
 
#This class handles transferring via SFTP           
class SftpChannel(TransferChannelBase):
    #start SFTP transfer 
    def channelOpened(self, data):
        print "sftpchannel channelopened"
        self.client = filetransfer.FileTransferClient()
        self.client.makeConnection(self)
        self.dataReceived = self.client.dataReceived
#        d = self.client.openFile(SRC, filetransfer.FXF_READ, {})
        # todo: select a destination directory for the video
        d = self.client.openFile(VIDEO, filetransfer.FXF_READ, {})
        d.addCallbacks(self.fileOpened, log.err)

    def fileOpened(self, result):
        # TODO: do something.
#        assert isinstance(result, filetransfer.ClientFile)
        pass

    def getDirectoryContents(self, path):
        print "getdirectorycontents"
        return self._remoteGlob(path)

        
    # Following methods are
    # copied from twisted.conch.scripts.cftp.py
    # which is a *nix only class
    def _remoteGlob(self, fullPath):
        logging.debug('looking up %s' % fullPath)
        head, tail = os.path.split(fullPath)
        if '*' in tail or '?' in tail:
            glob = 1
        else:
            glob = 0
        #Check if file or directory
        if tail and not glob:
            logging.debug("Opening dir")
            d = self.client.openDirectory(fullPath)
            d.addCallback(self._cbOpenList, '')
            d.addErrback(self._ebNotADirectory, head, tail)
        else:
            d = self.client.openDirectory(head)
            d.addCallback(self._cbOpenList, tail)
        return d

    def _cbOpenList(self, directory, glob):
        logging.debug("Got dir")
        files = []
        d = directory.read()
        d.addBoth(self._cbReadFile, files, directory, glob)
        return d

    def _ebNotADirectory(self, reason, path, glob):
        logging.debug("Not a dir")
        d = self.client.openDirectory(path)
        d.addCallback(self._cbOpenList, glob)
        return d

    def _cbReadFile(self, files, l, directory, glob):
        logging.debug("Reading file")
        if not isinstance(files, failure.Failure):
            l.extend(files)
            d = directory.read()
            d.addBoth(self._cbReadFile, l, directory, glob)
            return d
        else:
            reason = files
            reason.trap(EOFError)
            directory.close()
            return l

    def done(self, l):
        print ('done')
        global EXCODE
        EXCODE = 0

#This class retrieves the meta-data from a video file
class VideoData:
    def __init__(self, file):
        self.file = file
        self.title = ''
        self.artist = ''
        self.album = ''
        self.location = ''
        self.date = ''
        self.comment = ''
        self.raw_duration = 0
        self.duration = ''
        self.videowidth = 0
        self.videoheight = 0
        self.tags = {}
        self.mainloop = gobject.MainLoop()
        self.current = None

    def run(self):
        gobject.idle_add(self.checkIfValid)
        self.mainloop.run()

    #Currently this just prints the meta-data
    #Will have to get specific tags from discoverer object to store them
    def retrieveData(self, discoverer, ismedia):
        tags = discoverer.tags
        self.tags = tags
        if 'title' in tags:
            self.title = tags['title']
        if 'artist' in tags:
            self.artist = tags['artist']
        if 'album' in tags:
            self.album = tags['album']
        if 'location' in tags:
            self.location = tags['location']
        if 'date' in tags:
            self.date = tags['date']
        if 'comment' in tags:
            self.comment = tags['comment']
        self.raw_duration = max(discoverer.audiolength, discoverer.videolength)
        self.duration = discoverer._time_to_string(self.raw_duration)
        self.videowidth = discoverer.videowidth
        self.videoheight = discoverer.videoheight
#        self.body = 'Speaker: '+self.artist+'\nEvent: '+self.album+'\nDate:'+str(self.date)+'\nRoom: '+self.location+'\n\n'+self.comment
        self.current = None
        self.mainloop.quit()
        discoverer.set_state(gst.STATE_NULL)
        
    def getBody (self):
        return self.body
    
    #checks to make sure the file exists then creates Discoverer
    #object using the file path    
    def checkIfValid(self):
        if not os.path.isfile(self.file):
            gobject.idle_add(self._discover_one)
            return False
        self.current = Discoverer(self.file)
        # connect a callback on the 'discovered' signal
        self.current.connect('discovered', self.retrieveData)
        self.current.discover()
        return False
    
class DrupalNode:
    def __init__(self, title, body, username, password, site, filepath):
        self.node = {
                     'title': title,
                     'body': body,
                     'type': 'story',
                     'promote': False,
                     'name': username,
                     'language': 'en',
                     'status': 1,
                     'files': {}
                     }
        self.password = password
        self.timestamp = str(int(time.time()))
        if os.path.exists(filepath):
           self.file = filepath 
        self.server = xmlrpclib.ServerProxy(site, allow_none=True)
        try:
            connection = self.server.system.connect()
        except xmlrpclib.ProtocolError:
            try: 
                self.server = xmlrpclib.ServerProxy(site+'/xmlrpc', allow_none=True)
                connection = self.server.system.connect()
            except xmlrpclib.ProtocolError:
                try:
                    self.server = xmlrpclib.ServerProxy(site+'/services/xmlrpc', allow_none=True)
                    connection = self.server.system.connect()
                except xmlrpclib.ProtocolError:
                    print 'XMLRPC server not found'
                    sys.exit()
        session = self.server.user.login(connection['sessid'], username, self.password)
        if 'Wrong username or password.' in session:
            print session
            sys.exit()
        self.sessid = session['sessid']
        self.user = session['user']
        self.node['uid'] = self.user['uid']
        self.setupFile()
    
    def setupFile(self):
        fileName = os.path.basename(self.file)
        fileSize = os.path.getsize(self.file)
        fileMime = mimetypes.guess_type(self.file, False)
        rb = open(self.file, 'rb')
        file = rb.read()
        rb.close()
        self.fileNode = {
                'file': base64.b64encode(file),
                'filename': fileName,
                'filepath': 'sites/default/files/' + fileName,
                'filesize': fileSize,
                'timestamp': self.timestamp,
                'uid': self.user['uid'],
                'filemime': fileMime,
                }
    
    def saveFile (self):
        try:
            self.file = self.server.file.save (self.file)
            if 'Access denied' or 'Missing required arguments' in self.file:
                self.file = self.server.file.save (self.sessid, self.fileNode)
        except xmlrpclib.Fault:
            print 'Error saving file to server'
            sys.exit()
            
    def getDrupalFile (self):
        try:
            drupalFile = self.server.file.get (self.sessid, self.file)
        except xmlrpclib.Fault:
            print 'Error getting file info from server'
            sys.exit()
        nodeFile = {
                    'new': 1,
                    'fid': drupalFile['fid'],
                    'list': 0,
                    'weight': 0
                    }
        self.node['files'][self.file] = nodeFile
        
    
    def saveNode (self):
        try:
            save = self.server.node.save (self.node)
            if 'Access denied' or 'Missing required arguments' in save:
                save = self.server.node.save (self.sessid, self.node)
        except xmlrpclib.Fault:
            print 'Error saving file to server'
            sys.exit()
            
    def save (self):
        self.saveFile()
        self.getDrupalFile()
        self.saveNode()
            
if __name__ == '__main__':
    # sftp doesn't work
    # scp is untested (probably broken)
    # drupal is untested (probably works)
    drupal = False
    
    if '-u' in sys.argv:
        USER = sys.argv[sys.argv.index('-u')+1]
    if '-p' in sys.argv:
        PASS = sys.argv[sys.argv.index('-p')+1]
    if '--host' in sys.argv:
        HOST = sys.argv[sys.argv.index('--host')+1]
    if '-d' in sys.argv:
        VIDEO = sys.argv[sys.argv.index('-d')+1]
        SRC = VIDEO
    if '-drupal' in sys.argv:
        drupal = True
    
    if not (USER is None or PASS is None or HOST is None or VIDEO is None):
        if drupal:
            video = VideoData(VIDEO)
            video.run()
            node = DrupalNode (video.title, video.body, USER, PASS, HOST, VIDEO)
            node.save()
        else:
            protocol.ClientCreator(reactor, Transport).connectTCP(HOST, 22)
            reactor.run() #@UndefinedVariable
    else:
        print 'Please enter a username, password, host, and filepath'
        sys.exit()
    
#    if not USER is None:
    #Test scp/sftp upload
#        protocol.ClientCreator(reactor, Transport).connectTCP(HOST, 22)
#        reactor.run()
    
    #Test GstFile
#    video = VideoData(VIDEO)
#    video.run()
    
    
    #Test DrupalNode
#    node = DrupalNode ('Title', 'body', 'druapl', 'drupal', 'http://localhost')
#    node.save()
