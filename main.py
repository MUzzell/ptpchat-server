#!/usr/bin/python
#
# Experimental ptpchat-server (UDP)
# Very much wip
#
# TODO: Most verbs, a timeout on known_ips, threading.
#

import pdb, os, datetime, sys
import socket
import threading
import atexit

from listener_server import ListenerServer
from broadcast_server import BroadcastServer
from node_manager import NodeManager
from log_manager import LogManager

UDP_IP = "0.0.0.0"
UDP_PORT = 9001

MSG_TYPE = 'msg_type'
MSG_DATA = 'msg_data'

global known_ips
known_ips = []

base_routing_msg = {
    MSG_TYPE:'ROUTING', 
        MSG_DATA: {
            'users': [ ]}
    }

    
def setup():
    addr = (UDP_IP, UDP_PORT)
    logger = LogManager("ptpchat-server", "DEBUG")
    node_manager = NodeManager(logger)
    
    listener = ListenerServer(addr, logger = logger, node_manager = node_manager)
    broadcast = BroadcastServer(addr, logger=logger, node_manager = node_manager)
    
    listener_thread = threading.Thread(target=listener.serve_forever, name="Listener")
    listener_thread.daemon = True
    
    broadcast_thread = thread.Thread(target=broadcast.main_loop, name="Broadcast")
    broadcast_thread.daemon = True
    
    listener_thread.start()
    broadcast_thread.start()
    
    print "Listener Server running in thread:", server_thread.name
    
    
def shutdown():
    pass

if __name__ == '__main__':
	setup()
    atexit.register(shutdown)
