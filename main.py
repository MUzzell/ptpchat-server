#!/usr/bin/python
#
# Experimental ptpchat-server (UDP)
# Very much wip
#
# TODO: Most verbs, a timeout on known_ips, threading.
#

import pdb, os, datetime, sys, platform
import socket
import threading, time
import atexit

import signal

from listener_server import ListenerServer
from broadcast_server import BroadcastServer
from node_manager import NodeManager
from log_manager import LogManager

UDP_IP = "0.0.0.0"
UDP_PORT = 9001

MSG_TYPE = 'msg_type'
MSG_DATA = 'msg_data'

logger_name = "ptpchat-server"

global known_ips
known_ips = []

base_routing_msg = {
    MSG_TYPE:'ROUTING', 
        MSG_DATA: {
            'users': [ ]}
    }

def setup():
    global listener, broadcast
    addr = (UDP_IP, UDP_PORT)
    node_manager = NodeManager(logger = LogManager(logger_name, "DEBUG"))
    
    threading.current_thread().name = "Main"
    
    listener = ListenerServer(addr, 
        logger = LogManager(logger_name, "ListenerServer", "DEBUG"), 
        node_manager = node_manager)
    broadcast = BroadcastServer(addr, 
        logger = LogManager(logger_name, "BroadcastServer", "DEBUG"), 
        node_manager = node_manager)
    
    listener_thread = threading.Thread(target=listener.serve_forever, name="Listener")
    listener_thread.daemon = True
    
    broadcast_thread = threading.Thread(target=broadcast.start, name="Broadcast")
    broadcast_thread.daemon = True
    
    listener_thread.start()
    broadcast_thread.start()
 
        
def shutdown(signum, frame):
    global listener, broadcast, exit_flag
    threading.current_thread().name = "Main Shutdown"
    
    broadcast.stop()
    listener.shutdown()
    
    exit_flag.set()
    

if __name__ == '__main__':
    setup()
    
    signal.signal(signal.SIGINT, shutdown)
    exit_flag = threading.Event()
    exit_flag.clear()
    
    if platform.system() is 'Windows':
        while exit_flag.is_set() is False:
            exit_flag.wait(5)
    else:
        signal.pause()
