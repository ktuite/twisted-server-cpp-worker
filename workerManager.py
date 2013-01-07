from twisted.internet import protocol, defer, threads, utils, error
from twisted.protocols import basic
from twisted.internet.protocol import Factory


class WorkerProtocol(basic.LineReceiver):
    def __init__(self):
        print "init"
        self.queue = []

    # Don't need a connectionMade, nothing interesting happens on connection
    def connectionMade(self):
        print "[ATTENTION] connection made"
        self.factory.master.client = self

    def connectionLost(self, reason):
        #if reason.check("twisted.internet.error.ConnectionDone"):
        print "[ATTENTION] connection lost"
      
    def sendCommand(self, cmd, job):
        print "Sending this command [%s] to worker" % (cmd)
        self.queue.insert(0, job)
        self.sendLine(cmd)
        
    def lineReceived(self, response_line):
        print "Line received:", response_line
        if len(self.queue) > 0:
            job = self.queue.pop()
            job.callback(response_line)
        
class WorkerManager(object):
    def __init__(self, reactor):
        self.reactor = reactor
        self.client = None
        print "initializing client manager"
        
    @defer.inlineCallbacks
    def launchClient(self):
        yield utils.getProcessValue("workerclient", [])
        #yield utils.getProcessValue("python", ["workerClient.py", "8005"])
        
    def start(self):
        factory = Factory()
        factory.protocol = WorkerProtocol
        factory.master = self
        self.reactor.listenTCP(8005, factory)
        
        self.launchClient()
        
    def sendMessageToClient(self, message):
        job = defer.Deferred()
        self.client.sendCommand(message, job)        
        return job