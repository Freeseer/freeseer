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
from twisted.conch.ssh.common import NS
from twisted.internet import defer, protocol, reactor
import sys, os, getpass

USER = 'mhubbard'
HOST = 'localhost'

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
        self.openChannel(ScpChannel(2**16, 2**15, self))

#This class sets up a channel to be used by the SCPchannel
class TransferChannelBase(channel.SSHChannel):
    
    name = 'session'
    state = None
    todo = 0
    buf = ''
        
    def channelOpen(self, data):
        # Might display/process welcome screen
        self.welcome = data

        # Call our handler
        d = self.conn.sendRequest(self, 'exec', NS('scp'), wantReply=1)
        d.addCallbacks(self.channelOpened)
        
    def closed(self):
        self.loseConnection()
        reactor.stop()

#This class handles the actual SCP transferring
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
            self.buf += data
            if not self.buf.endswith('\n'):
                return
            b = self.buf
            self.buf = ''

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
            
if __name__ == '__main__':
    protocol.ClientCreator(reactor, Transport).connectTCP(HOST, 22)
    reactor.run()