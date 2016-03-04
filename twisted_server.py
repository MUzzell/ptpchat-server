
import pdb

from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol


class TestProtocol(DatagramProtocol):
    
    def datagramRecieved(self, data, (host, port)):
        print "received %r from %s:%d" % (data, host, port)
        self.transport.write(data, (host, port))
    
def startup():
    protocol = TestProtocol()
    
    port = reactor.listenUDP(9001, protocol, interface='127.0.0.1')
    
    print "Running on %s" % (port)
    
    reactor.run()

if __name__ == '__main__':
    startup()