
import socket, pdb, json, time
import threading.Thread

class BroadcastServer():

    loop_sleep = 2
    
    def __init__(self, logger = None, node_manager = None):
        self.logger = logger
        self.node_manager = node_manager
    
    def main_loop():
        while True:
            diff = time.clock()
            broadcast_hello()
            broadcast_routing()
            diff = BroadcastServer.loop_sleep - (time.clock() - diff)
            if diff > 0:
                time.sleep(diff)
            
    def broadcast_hello():
        pass
        
    def broadcast_routing():
        pass