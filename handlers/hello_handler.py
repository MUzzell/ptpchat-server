
from base_handler import BaseHandler
import time

import pdb

class HelloHandler(BaseHandler):

    VERSION = 'version'
    log_no_node_id = "HELLO, no 'node_id' in data, ignoring"
    log_node_id_invalid = "HELLO, invalid 'node_id', ignoring"
    log_node_id_same_as_server = "HELLO, invalid 'node_id', ignoring"
    
    log_adding_node = "HELLO, adding node: %s"
    log_updating_node = "HELLO, updating node: %s"
    
    def __init__(self, uuid, logger= None, node_manager= None, extras = None):
        BaseHandler.__init__(self, uuid, logger, node_manager)
        self.verb = 'HELLO'
        self.ttl = 1
        self.flood = False
        
        if extras is not None and HelloHandler.VERSION in extras:
            self.version = extras[HelloHandler.VERSION]
        else:
            self.version = 'ptpchat-server; 0.0'
    
    def handleVerb(self, data, addr, sock):
        
        if "node_id" not in data:
            self.logger.warning(HelloHandler.log_no_node_id)
            return 
            
        node_id = self.parse_uuid(data[BaseHandler.NODE_ID])
        
        if node_id is None:
            self.logger.warning(HelloHandler.log_node_id_invalid)
            return 
            
        if node_id == self.server_uuid:
            self.logger.warning(HelloHandler.log_node_id_same_as_server)
            return
            
        node = self.node_manager.get_nodes({BaseHandler.NODE_ID: node_id})
    
        if node is None or len(node) == 0 :
            self.logger.info(HelloHandler.log_adding_node % node_id)
            self.node_manager.add_node({BaseHandler.NODE_ID : node_id, BaseHandler.CLIENT_ADDR : addr, BaseHandler.LAST_SEEN : time.time() })
        else:
            self.logger.info(HelloHandler.log_updating_node % node_id)
            node = node[0]
            node['last_seen'] = time.time()
            self.node_manager.update_node(node)
            
    def buildMessage(self, data):
        
        return self.compile_message({ 
            BaseHandler.NODE_ID : "%s" % self.server_uuid,
            HelloHandler.VERSION : self.version })
            

        
