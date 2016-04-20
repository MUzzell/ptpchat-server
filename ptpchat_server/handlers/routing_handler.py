
from ptpchat_server.base.node import Node
from base_handler import BaseHandler
import time

import pdb

class RoutingHandler(BaseHandler):

    NODES = 'nodes'
    ADDRESS = 'address'

    log_invalid_nodes = "ROUTING, invalid 'nodes' element, ignoring"
    log_invalid_nodes_entry = "ROUTING, invalid node entry in 'nodes', skipping"
    log_unknown_node = "ROUTING, received message from unknown node, ignoring"
    log_updating_ttl = "ROUTING, updating ttl to for node %s"
    
    def __init__(self, logger= None, node_manager= None):
        BaseHandler.__init__(self, logger, node_manager)
        self.verb = 'ROUTING'
        self.ttl = 1
        self.flood = False
        
    def handleVerb(self, sender_id, data, client, factory):
    
        sender_node = None
        
        if RoutingHandler.NODES not in data or type(data[RoutingHandler.NODES]) is not list:
            self.logger.warning(RoutingHandler.log_invalid_nodes)
            return False
            
        nodes = self.node_manager.get_nodes({Node.NODE_ID : sender_id})
        
        if nodes is None or len(nodes) == 0:
            self.logger.warning(RoutingHandler.log_unknown_node)
            return False
        else:
            sender_node = nodes[0]
            
        for node in data[RoutingHandler.NODES]:
            node_id = None
            ttl = None
            if type(node) is not dict:
                self.logger.warning(RoutingHandler.log_invalid_nodes_entry)
                continue
                
            if Node.NODE_ID in node and Node.is_valid_node_id(node[Node.NODE_ID]):
                node_id = Node.parse_node_id(node[Node.NODE_ID])
            else:
                self.logger.warning(RoutingHandler.log_invalid_nodes_entry)
                continue
            
            if Node.TTL in node and type(node[Node.TTL]) is int:
                ttl = node[Node.TTL]
            else:
                self.logger.warning(RoutingHandler.log_invalid_nodes_entry)
                continue
                
            routing_node = None
            
            if node_id[1] in sender_node.connections and sender_node.connections[node_id[1]] == ttl:
                self.logger.debug("ROUTING ttl for node %s has not changed, ignoring" % node[Node.NODE_ID])
                continue
            
            nodes = self.node_manager.get_nodes({Node.BASE_ID : node_id[1]})
            
            if nodes is None or len(nodes) == 0:
                routing_node = self.addRoutingNode(node_id, ttl+1)
                sender_node.connections[routing_node.base_id] = ttl
            else:
                routing_node = nodes[0]
                sender_node.connections[routing_node.base_id] = ttl
                if routing_node.ttl > ttl:
                    self.logger.info(RoutingHandler.log_updating_ttl % routing_node.base_id)
                    routing_node.ttl = ttl+1
                    self.node_manager.update_node(routing_node)
            
            self.node_manager.update_node(sender_node)
             
    def addRoutingNode(node_id, ttl):
        pass
    
    def buildMessage(self, data, target_id = None, ttl=None, flood=None):
        
        nodes = [{Node.NODE_ID : x.node_id, Node.TTL : x.ttl} for x in self.node_manager.get_nodes(None) if x.ttl > 0]
        
        return self.compile_message({ 
            RoutingHandler.NODES : nodes}, target_id, ttl, flood)
            
            