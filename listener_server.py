
from SocketServer import ThreadedUDPServer

from message_handler import MessageHandler

class ListenerServer(ThreadedUDPServer):
    '''
    This explains abit about the reuse address
    http://stackoverflow.com/questions/15260558/python-tcpserver-address-already-in-use-but-i-close-the-server-and-i-use-allow
    '''
    def __init__(self, (host, port), logger = None, node_manager = None):
       
        self.logger = logger
        self.node_manager = node_manager
        
        ThreadedUDPServer.allow_reuse_address = True
        ThreadedUDPServer.__init__(self, (host, port), MessageHandler)
        