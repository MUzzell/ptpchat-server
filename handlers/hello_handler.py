
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
            self.logger.info("HelloHandler, invalid msg_data")
            
        if "node_id" not in data:
            self.logger.info("HelloHandler, no 'node_id' in data")
        
        node_id = self.parse_uuid(data["node_id"])
        
        if node_id is None:
            self.logger.warning("HelloHandler, 'node_id' invalid")

        node = self.node_manager.get_nodes({'node_id': node_id})
    
        if node is None or len(node) == 0 :
            self.node_manager.add_node({'node_id' : node_id, 'client_addr' : addr, 'last_seen' : time.time() })
        else:
            node[0]['last_seen'] = time.time()
            self.node_manager.update_node(node)
            
    def buildMessage(self, data):
        
        return self.compile_message({ 
            BaseHandler.NODE_ID : self.server_uuid,
            HelloHandler.VERSION : self.version })
            

        
