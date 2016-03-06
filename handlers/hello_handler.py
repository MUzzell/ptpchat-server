
from base_handler import BaseHandler
import time

import pdb

class HelloHandler(BaseHandler):
    
    def handleVerb(self, data, addr, sock):
        if data is None or type(data) is not dict:
            self.logger.info("HelloHandler, invalid msg_data")
            
        if "node_id" not in data:
            self.logger.info("HelloHandler, no 'node_id' in data")
        
        node_id = self.parse_uuid(data["node_id"])
        
        if node_id is None:
            self.logger.warning("HelloHandler, 'node_id' invalid")

        node = self.node_manager.get_nodes({'node_id': node_id})
    
        if node is None:
            self.node_manager.add_node({'node_id' : node_id, 'client_addr' : addr})
        else:
            node.last_seen = time.time()

        
