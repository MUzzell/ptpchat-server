
from SocketServer import ThreadingUDPServer

from message_handler import MessageHandler

class ListenerServer(ThreadingUDPServer):
    '''
    This explains abit about the reuse address
    http://stackoverflow.com/questions/15260558/python-tcpserver-address-already-in-use-but-i-close-the-server-and-i-use-allow
    '''
    def __init__(self, config, logger = None, node_manager = None):
       
        if logger is None or node_manager is None or config is None:
            raise AttributeError("ListenerServer Init, logger, config or node_manager is None")
       
        self.logger = logger
        self.node_manager = node_manager
        self.server_uuid = config.main.server_uuid
        
        ThreadingUDPServer.allow_reuse_address = True
        ThreadingUDPServer.__init__(self, 
            (config.main.listen_host, config.main.listen_port), MessageHandler)
        
    def serve_forever(self):
        self.logger.info("ListenerServer starting up")
        self.logger.debug("Listening on: %s:%d" % self.server_address)
        ThreadingUDPServer.serve_forever(self)
        
    def shutdown(self):
        self.logger.info("ListenerServer shutting down")
        ThreadingUDPServer.shutdown(self)
        
        