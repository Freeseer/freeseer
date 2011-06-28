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

from twisted.conch.ssh import transport, userauth, connection, channel, keys, common
from twisted.internet import defer, protocol, reactor
from twisted.python import log
from gst.extend.discoverer import Discoverer
import sys, os, getpass
import gobject
gobject.threads_init()
import pygst
pygst.require('0.10')

USER = 'mhubbard'
PASS = None
HOST = 'localhost'
SRC = 'test.txt'
DST = '.'
PROTOCOL = 'scp'
EXCODE = 1
VIDEO = '~/2011-05-28_-_2230_-_Hey.ogg'

#This class handles the encryption details with the server
class Transport(transport.SSHClientTransport):
    
    #Checks to see that the fingerprint key match's up with the server's
    def verifyHostKey(self, hostKey, fingerprint):
        if fingerprint != 'b1:94:6a:c9:24:92:d2:34:7c:62:35:b4:d2:61:11:84':
            return defer.fail(error.ConchError('bad key'))
        else:
            return defer.succeed(1)

    #Once secure create a new connection with the user's authentication
    def connectionSecure(self):
        self.requestService(UserAuth(USER, Connection()))
        
    #Stops the connection   
    def connectionLost(self, reason):
        reactor.stop()


#This class handles the SSH Authentication with either ssh keys or a user input password
class UserAuth(userauth.SSHUserAuthClient):
    
    def getPassword(self):
        return defer.succeed(getpass.getpass("%s@%s's password: " % (USER, HOST)))
            
    def getPublicKey(self):
        path = os.path.expanduser('~/.ssh/id_rsa') 
        if not os.path.exists(path) or self.lastPublicKey:
            #if the file doesn't exist, or we've tried a public key
            return
        return keys.Key.fromFile(filename=path+'.pub').blob()

    def getPrivateKey(self):
        path = os.path.expanduser('~/.ssh/id_rsa')
        return defer.succeed(keys.Key.fromFile(path).keyObject)

#This class opens the connection channels
class ClientConnection(connection.SSHConnection):

    def serviceStarted(self):
        if PROTOCOL == 'scp':
            self.openChannel(ScpChannel(2**16, 2**15, self))
        else:
            self.openChannel(SftpChannel(2**16, 2**15, self))
        self.openChannel(ScpChannel(2**16, 2**15, self))

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
        # Call our handler
        d = self.conn.sendRequest(self, type, common.NS(PROTOCOL), wantReply=1)
        d.addCallbacks(self.channelOpened, log.err)
        
    def closed(self):
        self.loseConnection()
        reactor.stop()

#This class handles transferring via SCP
class ScpChannel(TransferChannelBase):
    #start SCP transfer
    def channelOpened(self, data):
        self.write('\0')
        self.state = 'waiting'

    def dataReceived(self, data):
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
        self.client = filetransfer.FileTransferClient()
        self.client.makeConnection(self)
        self.dataReceived = self.client.dataReceived
        d = self.client.openFile(SRC, filetransfer.FXF_READ, {})
        d.addCallbacks(self.fileOpened, log.err)

    def fileOpened(self, rfile):
        rfile.getAttrs().addCallbacks(self.fileStatted, log.err, (rfile,))

    def fileStatted(self, attributes, rfile):
        rfile.readChunk(0, 4096).addCallbacks(self.did_read, self.failed_read,
                                              (rfile, 0, attributes['size']), {},  # did_read position/keyword args
                                              (rfile, 0), {}                       # failed_read position/keyword args
                                              )

    def did_read(self, data, file, position, todo):
        DST.write(data)
        todo -= len(data)
        position += len(data)
        if todo<=0:
            return self.done(position)
        file.readChunk(position, 4096).addCallbacks(self.did_read, log.err, (file, position, todo))

    def failed_read(self, failure, file, position):
        file.check(EOFError)

    def done(self, l):
        global EXCODE
        EXCODE = 0

#This class retrieves the metadata from a video file
class GstFile:
    def __init__(self, file):
        self.file = file
        self.mainloop = gobject.MainLoop()
        self.current = None

    def run(self):
        gobject.idle_add(self._discover_one)
        self.mainloop.run()

    #Currently this just prints the metadata
    #Will have to get specific tags from discoverer object to store them
    def _discovered(self, discoverer, ismedia):
        discoverer.print_info()
        self.current = None
        gobject.idle_add(self._discover_one)
    
    #checks to make sure the file exists then creates Discoverer
    #object using the file path    
    def _discover_one(self):
        if not os.path.isfile(self.file):
            gobject.idle_add(self._discover_one)
            return False
        print "Running on", self.file
        self.current = Discoverer(self.file)
        # connect a callback on the 'discovered' signal
        self.current.connect('discovered', self._discovered)
        self.current.discover()
        return False
            
if __name__ == '__main__':
    #Test scp/sftp upload
    #protocol.ClientCreator(reactor, Transport).connectTCP(HOST, 22)
    #reactor.run()
    
    #Test GstFile
    gstfile = GstFile(VIDEO)
    gstfile.run()  