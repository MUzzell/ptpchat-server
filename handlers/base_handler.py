
from uuid import UUID

class BaseHandler():
    
    def __init__(self, logger= None, node_manager= None):
        self.logger= logger
        self.node_manager= node_manager
        
    def handleVerb(self, data, addr, sock):
        self.logger.error("BaseHandler.handleVerb called!")
        
    def parse_uuid(self, uid):
        try:
            val = UUID(uid, version=4)
        except ValueError:
            return None
            
        if val.hex == uid:
            return val
        else:
            return None