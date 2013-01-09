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
        self.enqueue(cmd, job)

    def enqueue(self, cmd, job):
        print "enqueuing command [%s]\n" % cmd
        if not self.queue:
            self.sendLine(cmd)

        self.queue.insert(0, (cmd, job) )

    def lineReceived(self, response_line):
        print "Line received:", response_line
        if len(self.queue) > 0:
            _, job = self.queue.pop()
            job.callback(response_line)
            if self.queue:
                cmd, job = self.queue[-1]
                print "dequeuing command [%s]"
                self.sendLine(cmd)
        
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
