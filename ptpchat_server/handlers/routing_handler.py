
from ptpchat_server.base.node import Node
from base_handler import BaseHandler
import time

import pdb

class RoutingHandler(BaseHandler):

    NODES = 'nodes'
    ADDRESS = 'address'

    def __init__(self, uuid, logger= None, node_manager= None, extras = None):
        BaseHandler.__init__(self, uuid, logger, node_manager)
        self.verb = 'ROUTING'
        self.ttl = 1
        self.flood = False
        
    def handleVerb(self, data, addr, sock):
        pass
    
    def buildMessage(self, data, ttl=None, flood=None):
        
        nodes = [{Node.NODE_ID : "%s" % x.node_id, Node.TTL : x.ttl} for x in self.node_manager.get_nodes(None)]
        
        return self.compile_message({ 
            BaseHandler.NODE_ID : "%s" % self.server_uuid,
            RoutingHandler.NODES : nodes}, ttl, flood)
            