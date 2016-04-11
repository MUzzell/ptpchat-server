
from uuid import UUID

import json

class BaseHandler():
    
    MSG_TYPE = 'msg_type'
    MSG_DATA = 'msg_data'
    
    NODE_ID = 'node_id'
    CLIENT_ADDR = 'client_addr'
    LAST_SEEN = 'last_seen'
    
    TTL = 'ttl'
    FLOOD = 'flood'
    
    def __init__(self, uuid, logger= None, node_manager= None, extras = None):
        self.verb = None
        self.ttl = 1
        self.flood = False
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
        
    def send_message(self, msg, addr, sock):
        self.logger.debug("%s, Sending message to %s:%d" % self.verb, addr[0], addr[1])
        
        sock.sendto(msg, addr)
            
    def compile_message(self, data, ttl=None, flood=None):
        if ttl is None:
            ttl = self.ttl
        if flood is None:
            flood = self.flood
        return json.dumps({
            BaseHandler.TTL : ttl,
            BaseHandler.FLOOD : flood,
            BaseHandler.MSG_TYPE : self.verb, 
            BaseHandler.MSG_DATA : data})