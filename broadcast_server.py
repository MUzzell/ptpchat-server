
import socket, pdb, json, time
import threading

class BroadcastServer():

    loop_sleep = 2
    
    def __init__(self, (host, port), logger = None, node_manager = None):
        
        if logger is None or node_manager is None:
            raise AttributeError("BroadcastServer Init, logger or node_manager is None")
            
        if host is None or port is None:
            raise AttributeError("BroadcastServer Init, addr is not valid")
            
        self.host = host
        self.port = port
        
        self.run = threading.Event()
        self.run.set()
        logger.set_module_name("BroadcastServer")
        self.logger = logger
        self.node_manager = node_manager
        
    def start(self):
        self.logger.info("BroadcastServer starting up")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        self.main_loop(sock)
    
    def main_loop(self, sock):
        while self.run.is_set():
            diff = time.clock()
            self.broadcast_hello()
            self.broadcast_routing()
            diff = BroadcastServer.loop_sleep - (time.clock() - diff)
            if diff > 0:
                time.sleep(diff)
        
        #not being printed.. for some reason
        self.logger.debug("BroadcastServer exit loop, closing socket")
        sock.close()
        self.run.set()
                
    def stop(self):
        self.logger.info("BroadcastServer shutting down")
        self.run.clear()
        self.run.wait(3)    
            
    def broadcast_hello(self):
        pass
        
    def broadcast_routing(self):
        pass