
from SocketServer import ThreadingUDPServer

from message_handler import MessageHandler

class ListenerServer(ThreadingUDPServer):
    '''
    This explains abit about the reuse address
    http://stackoverflow.com/questions/15260558/python-tcpserver-address-already-in-use-but-i-close-the-server-and-i-use-allow
    '''
    def __init__(self, (host, port), logger = None, node_manager = None):
       
        if logger is None or node_manager is None:
            raise AttributeError("ListenerServer Init, logger or node_manager is None")
       
        logger.set_module_name("ListenerServer")
        self.logger = logger
        self.node_manager = node_manager
        
        ThreadingUDPServer.allow_reuse_address = True
        ThreadingUDPServer.__init__(self, (host, port), MessageHandler)
        
    def shutdown(self):
        self.logger.info("ListenerServer shutting down")
        ThreadingUDPServer.shutdown(self)
        
        