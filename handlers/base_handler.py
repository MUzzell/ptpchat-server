
class BaseHandler():
    
    def __init__(self, logger= None, node_manager= None):
        self.logger= logger
        self.node_manager= node_manager
        
    def handleVerb(self, data, addr, sock):
        self.logger.error("BaseHandler.handleVerb called!")