from twisted.web.resource import Resource
from twisted.web import server, http, static
from twisted.python import log
from twisted.internet import defer, utils
import random

###################################
#### Root and utility resources ###
###################################

class RootResource(Resource):
    def __init__(self):
        Resource.__init__(self)

        # a Resource is a thing that handles your web request. 
        # here's where you define which url maps to which resource.
        self.putChild('random', ComputeRandomNumberResource())
        self.putChild('launch', LaunchResource())
        
# just a random random number generator resource... 
class ComputeRandomNumberResource(Resource):
    def __init__(self):
        Resource.__init__(self)
        
    def render_GET(self, request):
        rand = random.random()
        return "random number: %f" % rand

# a resource showing getProcessOutput and getProcessValue
class LaunchResource(Resource):
    def __init__(self):
        Resource.__init__(self)
        
    def render_GET(self, request):

        # Make a helper function inside the get request
        # that you can use inline callbacks in.
        # I've had bad luck putting the inlineCallbacks decorator 
        # on the render_GET/render_POST methods themselves.
        @defer.inlineCallbacks
        def _doWork():

            # only one 'word' can be in the command. 
            # everything else gets split up and put in the args array
            command = "pwd"
            args = [] 
        
            # run another command with getProcessOutput [to capture the stdout output]
            # or with getProcessValue [to just capture the exit code of the command]
            out = yield utils.getProcessOutput("pwd", [])
            val = yield utils.getProcessValue("pwd", [])

            # printing is the same as logging
            print "getProcessOutput:", out
            print "getProcessValue:", val
        
            # here's how you get stuff to display back in the web browser
            request.write("getProcessOutput: %s" % out)

            # you can do as many request.writes as you like, whenever/whereever
            request.write("<br />getProcessValue: %d" % val)

            # finish the request so the browser doesn't expect more
            request.finish()
            
            # how you finish up a method that has the @defer.inlineCallbacks decorator
            defer.returnValue(None)
            
        # now we call the helper function!
        _doWork()

        # and return this funny thing!
        return server.NOT_DONE_YET
        
##########################
#### Main! ###############
#### Go, little server! ##
##########################

if __name__ == "__main__":
    from twisted.internet import reactor  
    from sys import stdout
    import sys
        
    # logging is pretty helpful! 
    # sets it up so print statements get logged along with other various messages
    log.startLogging(stdout)
    
    # set up the server on a specific port with a specific root resource
    reactor.listenTCP(8080, server.Site(RootResource()))

    # start it running!
    log.msg("running...")
    reactor.run()
