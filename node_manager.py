
import threading

class NodeManager():
    
    def __init__(self, logger = None):
    
        if logger is None:
            raise AttributeError("NodeManager Init, logger is None")
       
        self.logger = logger
        self.monitor = ReadMonitor()
        
        self.nodes = {}
        
    '''
    Nodes are identifies by their 'node_id' and NOT their 
    ssl material.
    If we are adding a node that has been seen bofore, update
    '''
    def add_node(self, node):
        if 'node_id' not in node:
            raise AttributeError("NodeManager, adding node without node_id")
        if 'client_addr' not in node:
            raise AttributeError("NodeManager, adding node without client_addr")

        if len(self.get_nodes(node)) > 0: 
            self.logger.info("tried to add node that is already registered")
            return node

        node_id = node['node_id']
        self.monitor.start_write()
        self.nodes[node_id] = node
        self.monitor.end_write()
        
        return None
        
    def update_node(self, node):
        if 'node_id' not in node:
            raise AttributeError("NodeManager, updating node without node_id")
        self.monitor.start_read()
        
        if node['node_id'] not in self.nodes:
            self.monitor.end_read()
            raise AttributeError("NodeManager, updating node not in nodes!")
        
        self.monitor.end_read()
        self.monitor.start_write()
        self.nodes[node['node_id']] = node
        self.monitor.end_write()
        
        return None
        
        
    def drop_node(self, node):
        pass
    
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

    def __matches(self, node, filter):
        if 'node_id' in filter:
            node = node if filter['node_id'] == node else None
        return node is not None
         
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
       

