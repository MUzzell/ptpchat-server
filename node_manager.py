
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
        if 'node_id' not in node:
            raise AttributeError("NodeManager, adding node without node_id")
        if 'client_addr' not in node:
            raise AttributeError("NodeManager, adding node without client_addr")

        if self.get_nodes(node) is not None:
            self.logger.info("tried to add node that is already registered")

        self.monitor.start_write()
        self.nodes ++ [node]
        self.monitor.end_write()
        
    def drop_node(self, node):
        pass
    
    def get_channels(self):
        pass
       
    def get_nodes(self, filter):
        self.monitor.start_read()
        nodes = [x for x in self.nodes if self.node_matches(x, filter)]
        self.monitor.end_read()
        return nodes

    def matches(self, node, filter):
        if 'node_id' in filter:
            node = node if filter['node_id'] == node['node_id'] else None
        return node is not None
         
class ReadMonitor():
    
    def __init__(self, lock):
        self.count = 0
        self.internal_lock = threading.Lock()
        self.write_event = threading.Event()
        self.write_event.set()

    def start_read(self):
        #potential race condition?
        while self.write_event.is_set() is False:
            self.write_event.wait()
        self.internal_lock.acquire()
     
        self.count += 1

        self.internal_lock.release()

    def end_read(self):
        self.internal_lock.acquire()
        self.count -= 1
        self.internal_lock.release()

    def start_write(self):
        self.write_event.wait()
            
        while self.count > 0:
            time.sleep(0.2 * self.count)
        
        self.internal_lock.acquire()
        if self.count == 0:
            self.write_event.clear()
        
        self.internal_lock.release()       

    def end_write(self):
        self.write_event.set()

