
import socket, pdb, json, time
import threading
import handlers
import sched

#don't like this being here.. :(
__handler_classes__ = {
    "HELLO" : handlers.HelloHandler,
    "ROUTING" : handlers.RoutingHandler,
    "CONNECT" : handlers.ConnectHandler
}

class BroadcastServer():

    
    log_start_server = "BroadcastServer starting up"
    log_stop_server = "BroadcastServer shutting down"
    
    def __init__(self, socket, config, logger = None, node_manager = None):
        
        if logger is None or node_manager is None or config is None:
            raise AttributeError("BroadcastServer Init, logger, config or node_manager is None")
          
        self.sock = socket
        self.server_uuid = config.main.server_uuid
        
        self.node_cutoff = config.broadcast.node_cutoff
        self.loop_sleep = config.broadcast.loop_sleep
        
        global __handler_classes__
        
        self.handlers = __handler_classes__
        
        for handler in self.handlers:
            self.handlers[handler] = self.handlers[handler](self.server_uuid, logger, node_manager)
            
        self.run = threading.Event()
        self.run.set()
        self.logger = logger
        self.node_manager = node_manager
        
    def start(self):
        self.logger.info(BroadcastServer.log_start_server)
        self.main_loop(self.sock)
    
    def main_loop(self, sock):
        while self.run.is_set():
            diff = time.time()
            self.broadcast_hello()
            self.broadcast_routing()
            self.process_nodes()
            diff = self.loop_sleep - (time.time() - diff)
            if diff > 0:
                time.sleep(diff)
        
        self.run.set()
                
    def stop(self):
        self.logger.info(BroadcastServer.log_stop_server)
        self.run.clear()
        self.run.wait(3)    
        
    def process_nodes(self):
        self.logger.debug("pruning node list")
        nodes = self.node_manager.get_nodes({'last_seen_lt' : time.time() - self.node_cutoff})
        
        if nodes is not None and len(nodes) > 0:
            for node in nodes:
                self.node_manager.drop_node(node)
            
    def broadcast_hello(self):
        
        nodes = self.node_manager.get_nodes(None)
        self.logger.debug("Sending HELLO to %d nodes" % len(nodes))
        
        for node in nodes:
            self.sock.sendto(self.handlers['HELLO'].buildMessage(node), node['client_addr'])
        
    def broadcast_routing(self):
        nodes = self.node_manager.get_nodes(None)
        self.logger.debug("Sending ROUTING to %d nodes" % len(nodes))
        for node in nodes:
            self.sock.sendto(self.handlers['ROUTING'].buildMessage(node), node['client_addr'])
