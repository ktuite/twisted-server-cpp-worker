from twisted.web.resource import Resource
from twisted.web import server, http, static
from twisted.python import log
from twisted.internet import defer, utils
import os
import re
import time
import struct

import workerManager
cm = None

###################################
#### Root and utility resources ###
###################################

class RootResource(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.putChild('random', ComputeRandomResource())
        
class ComputeRandomResource(Resource):
    def __init__(self):
        Resource.__init__(self)
        
    def render_GET(self, request):
        @defer.inlineCallbacks
        def _doWork():        
        
            res = yield cm.sendMessageToClient("random")
        
            request.write("result: " + str(res))
            request.finish()
            
            defer.returnValue(None)
            
        _doWork()
        return server.NOT_DONE_YET
        
##########################
#### Main! ###############
#### Go, little server! ##
##########################

if __name__ == "__main__":
    from twisted.internet import reactor  
    from sys import stdout
    import sys
        
    log.startLogging(stdout)

    cm = workerManager.WorkerManager(reactor)
    cm.start()
    
    reactor.listenTCP(8080,server.Site(RootResource()))

    log.msg("running...")
    reactor.run()
