
from base_handler import BaseHandler
import time

import pdb

class HelloHandler(BaseHandler):

    VERSION = 'version'

    def __init__(self, uuid, logger= None, node_manager= None, extras = None):
        BaseHandler.__init__(self, uuid, logger, node_manager)
        self.verb = 'HELLO'
        
        if extras is not None and HelloHandler.Version in extras:
            self.version = extras[HelloHandler.Version]
        else:
            self.version = 'ptpchat-server; 0.0'
    
    def handleVerb(self, data, addr, sock):
        if data is None or type(data) is not dict:
            self.logger.warning("HelloHandler, invalid msg_data")
            return
            
        if "node_id" not in data:
            self.logger.warning("HelloHandler, no 'node_id' in data")
            return 
            
        node_id = self.parse_uuid(data["node_id"])
        
        if node_id is None:
            self.logger.warning("HelloHandler, 'node_id' invalid")
            return 
            
        node = self.node_manager.get_nodes({'node_id': node_id})
    
        if node is None or len(node) == 0 :
            self.logger.info("HelloHandler, adding node %s" % node_id)
            self.node_manager.add_node({'node_id' : node_id, 'client_addr' : addr, 'last_seen' : time.time() })
        else:
            self.logger.info("HelloHandler, updating node %s" % node_id)
            node = node[0]
            node['last_seen'] = time.time()
            self.node_manager.update_node(node)
            
    def buildMessage(self, data):
        
        return self.compile_message({ 
            BaseHandler.NODE_ID : self.server_uuid,
            HelloHandler.VERSION : self.version })
            

        
