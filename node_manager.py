
import threading

class NodeManager():
    
    def __init__(self, logger = None):
    
        if logger is None:
            raise AttributeError("NodeManager Init, logger is None")
       
        logger.set_module_name("NodeManager")
        self.logger = logger
        self.lock = threading.Lock
        
        self.nodes = []
        
    '''
    Nodes are identifies by their 'node_id' and NOT their 
    ssl material.
    If we are adding a node that has been seen bofore, update
    '''
    def add_node(self, node):
        pass
        
    def drop_node(self, node):
        pass
    
    def get_channels(self):
        pass
       
    def get_nodes(self):
        pass
        