#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import sys
import random

class EchoClient(LineReceiver):
    end="Bye-bye!"
    def connectionMade(self):
        self.sendLine("Hello! A connection has been made!")
        
    def connectionLost(self, reason):
        print "connection lost inside echoclient line receiever"
        print "reason:", reason

    def lineReceived(self, line):
        print "receive:", line
        if line==self.end:
            self.transport.loseConnection()
        elif line=="random":
            self.sendLine(str(random.random()))

class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
        reactor.stop()

def main(port):
    factory = EchoClientFactory()
    reactor.connectTCP('localhost', port, factory)
    reactor.run()

if __name__ == '__main__':
    port = int(sys.argv[1])
    main(port)
