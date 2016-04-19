
import threading, re

from ptpchat_server.base.node import Node

class NodeManager():

    log_deleted_node = "NodeManager, deleted node: %s"
    log_add_node_already_exists = "NodeManager, tried to add node that already exists: %s" 
      
    def __init__(self, config, logger):
    
        if config is None or logger is None:
            raise AttributeError("NodeManager Init, logger is None")
       
        self.logger = logger
        self.monitor = ReadMonitor()
        
        self.nodes = {}
        
        self.local_node = Node(config.main.server_id, {
            Node.VERSION : config.main.version,
            Node.ATTRIBUTES : {Node.NODE_TYPE : Node.NODE_TYPE_SERVER}
            })
       
    def update_nodes(self):
        self.logger.debug("pruning node list")
        nodes = self.get_nodes({'last_seen_lt' : time.time() - self.node_cutoff})
        
        if nodes is not None and len(nodes) > 0:
            for node in nodes:
                self.drop_node(node)
    
    '''
    An acceptable node is one where either:
        * Its TTL is one
        * Sent us a ROUTING message to the node (with the lowest TTL)
    '''
    def get_node_for_target(self, target_node):
        node = None
        
        nodes = self.get_nodes({Node.TTL : 1})
        
        if nodes is None or len(nodes) == 0:
            return node
            
        if target_node in nodes:
            return target_node
            
        nodes = [n for n in nodes if node.connects_to(target_id)]
        
        if len(nodes) == 0:
            return node
            
        sorted(nodes, key=lambda x: x.ttl)
            
        return nodes[0]
    
    def add_node(self, node_data):
          
        if Node.NODE_ID not in node_data or not Node.is_valid_node_id(node_data[Node.NODE_ID]):
            raise AttributeError("NodeManager, invalid node_id in add_node")
            
        node = Node(node_data[Node.NODE_ID], node_data)
        
        if len(self.get_nodes(node_data)) > 0: 
            self.logger.info(NodeManager.log_add_node_already_exists % node_data[Node.NODE_ID])
            return node
            
        self.monitor.start_write()
        self.nodes[node.base_id] = node
        self.monitor.end_write()
        
        return node
        
    def update_node(self, node):
    
        if type(node) is not Node:
            raise AttributeError("NodeManager, invalid node in update")
        
        self.monitor.start_read()
        
        if node.node_id not in self.nodes:
            self.monitor.end_read()
            raise AttributeError("NodeManager, updating node not in nodes!")
        
        self.monitor.end_read()
        self.monitor.start_write()
        self.nodes[node.base_id] = node
        self.monitor.end_write()
        
        return None
        
        
    def drop_node(self, node):
    
        if type(node) is not Node:
            raise AttributeError("NodeManager, invalid node in update")
        
        base_id = node.base_id
        
        self.monitor.start_read()
        if base_id not in self.nodes:
            self.monitor.end_read()
            raise AttributeError("NodeManager, node_id not found!")
        
        self.monitor.end_read()
        self.monitor.start_write()
        del self.nodes[base_id]
        self.monitor.end_write()
        self.logger.info(NodeManager.log_deleted_node % node_id)
    
    def get_channels(self):
        pass
       
    def get_nodes(self, filter):
    
        self.monitor.start_read()
        if filter is None:
            nodes = self.nodes.values()
        else:
            nodes = [self.nodes[x] for x in self.nodes if self.__matches(x, filter)]
        self.monitor.end_read()
        return nodes

    #MUST have read lock!!!
    def __matches(self, node, filter):
        return_node = None
        node = self.nodes[node]
        if Node.NODE_ID in filter:
            return_node = node if filter[Node.NODE_ID] == node.node_id else None
        if Node.BASE_ID in filter:
            return_node = node if filter[Node.BASE_ID] == node.base_id else None
        if Node.TTL in filter:
            return_node = node if filter[Node.TTL] == node.ttl else None
        if 'excluding_base_id' in filter:
            return_node = node if filter[Node.BASE_ID] != node.base_id else None
        if 'last_seen_lt' in filter:
            return_node = node if filter['last_seen_lt'] > node.last_seen else None
        if 'last_seen_gt' in filter:
            return_node = node if filter['last_seen_gt'] < node.last_seen else None
        return return_node is not None
         
class ReadMonitor():
    
    def __init__(self):
        self.count = 0
        
        self.write_cond = threading.Condition()
        
    def start_read(self):
        self.write_cond.acquire()
        self.count += 1
        self.write_cond.release()

    def end_read(self):
        self.write_cond.acquire()
        self.count -= 1
        if self.count == 0:
            self.write_cond.notify()
        self.write_cond.release()

    def start_write(self):
    
        self.write_cond.acquire()
        while not self.count == 0:
            self.write_cond.wait(0.5)

    def end_write(self):
        self.write_cond.notify()
        self.write_cond.release()
       

