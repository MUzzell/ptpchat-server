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
file_name = '/etc/var/log/ptpchat-server/ptpchat-server.log'

global known_ips
known_ips = []

base_routing_msg = {
    MSG_TYPE:'ROUTING', 
        MSG_DATA: {
            'users': [ ]}
    }

def setup(server_uuid):
    global listener, broadcast
    addr = (UDP_IP, UDP_PORT)
    node_manager = NodeManager(logger = LogManager(
        logger_name,
        file_name,
        module_name='node_manager', 
        log_level="DEBUG"))
    
    threading.current_thread().name = "Main"
    
    listener = ListenerServer(addr, server_uuid,
        logger = LogManager(
            logger_name,
            file_name,
            module_name = "ListenerServer", 
            log_level = "DEBUG"), 
        node_manager = node_manager)
    listener.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcast = BroadcastServer(listener.socket, server_uuid,
        logger = LogManager(
            logger_name,
            file_name,
            module_name = "BroadcastServer", 
            log_level = "DEBUG"), 
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
    setup('5f715c17-4a41-482a-ab1f-45fa2cdd702b')
    
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    exit_flag = threading.Event()
    exit_flag.clear()
    
    if platform.system() is 'Windows':
        while exit_flag.is_set() is False:
            try:
                exit_flag.wait(5)
            except IOError:
                pass
    else:
        signal.pause()
