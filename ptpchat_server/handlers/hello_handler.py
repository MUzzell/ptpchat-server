
from ptpchat_server.base.node import Node
from base_handler import BaseHandler
import time

import pdb

class HelloHandler(BaseHandler):

    VERSION = 'version'
    ATTRIBUTES = 'attributes'
    log_invalid_sender_id = "HELLO, invalid 'sender_id', ignoring"
    log_invalid_attributes = "HELLO, invalid 'attributes', ignoring"
    
    log_adding_node = "HELLO, adding node: %s"
    log_updating_node = "HELLO, updating node: %s"
    
    def __init__(self, logger= None, node_manager= None):
        BaseHandler.__init__(self, logger, node_manager)
        self.verb = 'HELLO'
        self.ttl = 1
        self.flood = False
        
    def handleVerb(self, sender_id, data, client, factory):
        
        if sender_id is None:
            self.logger.warning(HelloHandler.log_invalid_sender_id)
            return False
            
        if sender_id == self.node_manager.local_node.node_id:
            self.logger.warning(HelloHandler.log_invalid_sender_id)
            return False
            
        if Node.ATTRIBUTES in data and type(data[Node.ATTRIBUTES]) is not dict:
            self.logger.warning(HelloHandler.log_invalid_attriubtes)
            return False
            
        nodes = self.node_manager.get_nodes({Node.NODE_ID: sender_id})
        
        node = None
    
        if nodes is None or len(nodes) == 0 :
            self.logger.info(HelloHandler.log_adding_node % sender_id)
            node = self.node_manager.add_node({
                Node.NODE_ID : sender_id, 
                Node.TTL : 1,
                Node.LAST_SEEN : time.time(), 
                Node.ATTRIBUTES : data[Node.ATTRIBUTES] if Node.ATTRIBUTES in data else None,
                Node.VERSION : data[Node.VERSION] if Node.VERSION in data else None})
        else:
            self.logger.info(HelloHandler.log_updating_node % sender_id)
            node = nodes[0]
            node.last_seen = time.time()
            node.ttl = 1
            self.node_manager.update_node(node)
        
        self.logger.debug("Attributing client %s:%d to node %s" % (client.addr.host, client.addr.port, node.node_id))
        client.set_node(node)
        
        self.logger.debug("Sending response HELLO to node %s" % node.node_id);
        client.sendString(self.buildMessage(None))
            
        return True
            
    def buildMessage(self, data, target_id = None, ttl=None, flood=None):
        
        return self.compile_message({ 
            HelloHandler.VERSION : self.node_manager.local_node.version,
            HelloHandler.ATTRIBUTES : self.node_manager.local_node.attributes}, target_id, ttl, flood)
            

        
