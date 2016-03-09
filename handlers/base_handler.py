
from uuid import UUID

import json

class BaseHandler():
    
    MSG_TYPE = 'msg_type'
    MSG_DATA = 'msg_data'
    
    NODE_ID = 'node_id'
    
    def __init__(self, uuid, logger= None, node_manager= None, extras = None):
        self.verb = None
        self.server_uuid = uuid
        self.logger= logger
        self.node_manager= node_manager
        
    def handleVerb(self, data, addr, sock):
        self.logger.error("BaseHandler.handleVerb called!")
        
    def buildMessage(self, data):
        self.logger.error("BaseHandler.buildVerb called!")
        
    def parse_uuid(self, uid):
        try:
            val = UUID(uid, version=4)
        except ValueError:
            self.logger.debug("given uid incorrect, %s" % ValueError)
            return None
        return val  
            
    def compile_message(self, data):
        return json.dumps({BaseHandler.MSG_TYPE : self.verb, BaseHandler.MSG_DATA : data})