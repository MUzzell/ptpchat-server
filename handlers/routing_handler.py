
from base_handler import BaseHandler
import time

import pdb

class RoutingHandler(BaseHandler):

    NODES = 'nodes'
    ADDRESS = 'address'

    def __init__(self, uuid, logger= None, node_manager= None, extras = None):
        BaseHandler.__init__(self, uuid, logger, node_manager)
        self.verb = 'ROUTING'
        
    def handleVerb(self, data, addr, sock):
        pass
    
    def buildMessage(self, data):
        
        nodes = [{BaseHandler.NODE_ID : "%s" % x[BaseHandler.NODE_ID], RoutingHandler.ADDRESS : "%s:%d" % x[BaseHandler.CLIENT_ADDR]} for x in self.node_manager.get_nodes(None)]
        
        return self.compile_message({ 
            BaseHandler.NODE_ID : "%s" % self.server_uuid,
            RoutingHandler.NODES : nodes})
            