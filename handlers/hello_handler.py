
from base_handler import BaseHandler
import time

import pdb

class HelloHandler(BaseHandler):

    VERSION = 'version'
    ATTRIBUTES = 'attributes'
    log_invalid_sender_id = "HELLO, invalid 'sender_id', ignoring"
    log_invalid_sender_id = "HELLO, invalid 'attributes', ignoring"
    
    log_adding_node = "HELLO, adding node: %s"
    log_updating_node = "HELLO, updating node: %s"
    
    def __init__(self, logger= None, node_manager= None, extras = None):
        BaseHandler.__init__(self, logger, node_manager)
        self.verb = 'HELLO'
        self.ttl = 1
        self.flood = False
        
        if extras is not None and HelloHandler.VERSION in extras:
            self.version = extras[HelloHandler.VERSION]
        else:
            self.version = 'ptpchat-server; 0.0'
    
    def handleVerb(self, sender_id, data, client, factory):
        
        if sender_id is None:
            self.logger.warning(HelloHandler.log_invalid_sender_id)
            return False
            
        if sender_id == self.node_manager.local_node[BaseHandler.NODE_ID]:
            self.logger.warning(HelloHandler.log_invalid_sender_id)
            return False
            
        if HelloHandler.ATTRIBUTES in data and type(data[HelloHandler.ATTRIBUTES]) is not dict:
            self.logger.warning(HelloHandler.log_attriubtes_invalid)
            return False
            
        node = self.node_manager.get_nodes({BaseHandler.NODE_ID: sender_id})
    
        if node is None or len(node) == 0 :
            self.logger.info(HelloHandler.log_adding_node % node_id)
            self.node_manager.add_node({
                BaseHandler.NODE_ID : sender_id, 
                BaseHandler.LAST_SEEN : time.time(), 
                NodeManager.ATTRIBUTES : data[NodeManager.ATTRIBUTES] })
        else:
            self.logger.info(HelloHandler.log_updating_node % node_id)
            node = node[0]
            node['last_seen'] = time.time()
            self.node_manager.update_node(node)
            
        return True
            
    def buildMessage(self, data, ttl=None, flood=None):
        
        return self.compile_message({ 
            BaseHandler.NODE_ID : "%s" % self.server_uuid,
            HelloHandler.VERSION : self.version }, ttl, flood)
            

        
