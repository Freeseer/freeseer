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

from twisted.conch.ssh import transport, userauth, connection, channel, keys, common, filetransfer
from twisted.internet import defer, protocol, reactor
from twisted.python import log
from twisted.conch import error
import sys, os, getpass
import xmlrpclib, time
import gobject
gobject.threads_init()
import pygst
pygst.require('0.10')
from gst.extend.discoverer import Discoverer

USER = 'mrjhubba'
PASS = None
HOST = '134.117.29.70'
SRC = 'new-file'
DST = 'test/'
PROTOCOL = 'sftp'
EXCODE = 1
VIDEO = '/home/mathieu/Videos/2011-04-06_-_1459_-_T103_-_Thanh_Ha_-_Intro_to_Freeseer.ogg'

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
        try:
            passwd = defer.succeed(getpass.getpass("%s@%s's password: " % (USER, HOST)))
        except GetPassWarning:
            print "Ooop that was not a valid password, %s" % passwd
        return passwd
            
    def getPublicKey(self):
        print ('getPublicKey')
#        path = os.path.expanduser('~/.ssh/id_rsa') 
#        if not os.path.exists(path) or self.lastPublicKey:
            #if the file doesn't exist, or we've tried a public key
        return
#        return keys.Key.fromFile(filename=path+'.pub').blob()

    def getPrivateKey(self):
        print ('getPrivateKey')
#        path = os.path.expanduser('~/.ssh/id_rsa')
        return #defer.succeed(keys.Key.fromFile(path).keyObject)

#This class opens the connection channels
class ClientConnection(connection.SSHConnection):

    def serviceStarted(self):
        print ('servicesStarted')
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
        print ('channelOpen')
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
        print ('closed')
        self.loseConnection()
        reactor.stop()

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
        print ('SFTP Opened')
        self.client = filetransfer.FileTransferClient()
        self.client.makeConnection(self)
        #self.dataReceived = self.client.dataReceived
        #d = self.client.openFile(SRC, filetransfer.FXF_READ, {})
        #d.addCallbacks(self.fileOpened, log.err)

    def getDirectoryContents(self, path):
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
        self.tags = {}
        self.mainloop = gobject.MainLoop()
        self.current = None

    def run(self):
        gobject.idle_add(self.checkIfValid)
        self.mainloop.run()

    #Currently this just prints the meta-data
    #Will have to get specific tags from discoverer object to store them
    def retrieveData(self, discoverer, ismedia):
        self.tags = discoverer.tags
        self.current = None
    
    #checks to make sure the file exists then creates Discoverer
    #object using the file path    
    def checkIfValid(self):
        if not os.path.isfile(self.file):
            gobject.idle_add(self._discover_one)
            return False
        print "File Path: ", self.file
        self.current = Discoverer(self.file)
        # connect a callback on the 'discovered' signal
        self.current.connect('discovered', self.retrieveData)
        self.current.discover()
        return False
    
class DrupalNode:
    def __init__(self, title, body, path, ntype, uid, username, password, api, site):
        self.title = title
        self.body = body
        self.path = path
        self.type = ntype
        self.uid = uid
        self.name = username
        self.password = password
        self.api = api
        self.promote = False
        self.site = site
    
    def connect(self):
        sessid, user = self.site.system.connect()
        
    def userAuth (self):
        self.login = drupal.user.login(api,user['sessid'],username,password)
    
    def save (self):
        self.site.node.save(login['sessid'], self)
            
if __name__ == '__main__':
    #Test scp/sftp upload
    #protocol.ClientCreator(reactor, Transport).connectTCP(HOST, 22)
    #reactor.run()
    
    #Test GstFile
    #video = VideoData(VIDEO)
    #video.run()
    #print video.tags
    
    
    #Test DrupalNode
    node = DrupalNode ('Title', 'body', '.', 'page', 1, 'drupal', 'drupal', '13894a48c4e071fca0e68602106df97e', xmlrpclib.ServerProxy('http://localhost/xmlrpc'))
    node.connect()
    node.save()