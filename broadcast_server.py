
import socket, pdb, json, time
import threading
import handlers

#don't like this being here.. :(
__handler_classes__ = {
    "HELLO" : handlers.HelloHandler
}

class BroadcastServer():

    loop_sleep = 2
    
    def __init__(self, socket, server_uuid, logger = None, node_manager = None):
        
        if logger is None or node_manager is None:
            raise AttributeError("BroadcastServer Init, logger or node_manager is None")
            
        if host is None or port is None:
            raise AttributeError("BroadcastServer Init, addr is not valid")
            
        self.sock = sock
        self.server_uuid = server_uuid
        global __handler_classes__
        
        self.handlers = __handler_classes__
        
        for handler in self.handlers:
            self.handlers[handler] = self.handlers[handler](server_uuid, logger, node_manager)
        
        self.run = threading.Event()
        self.run.set()
        self.logger = logger
        self.node_manager = node_manager
        
    def start(self):
        self.logger.info("BroadcastServer starting up")
        self.main_loop(self.sock)
    
    def main_loop(self, sock):
        while self.run.is_set():
            diff = time.time()
            self.broadcast_hello()
            self.broadcast_routing()
            diff = BroadcastServer.loop_sleep - (time.time() - diff)
            if diff > 0:
                time.sleep(diff)
        
        self.logger.debug("BroadcastServer exit loop, closing socket")
        sock.close()
        self.run.set()
                
    def stop(self):
        self.logger.info("BroadcastServer shutting down")
        self.run.clear()
        self.run.wait(3)    
            
    def broadcast_hello(self):
        
        nodes = self.node_manager.get_nodes(None)
        self.logger.debug("Sending HELLO to %d nodes" % len(nodes))
        
        for node in nodes:
            
            self.sock.sendto(handlers['HELLO'].buildMessage(node), node['client_addr'])
            
        
        
    def broadcast_routing(self):
        pass
