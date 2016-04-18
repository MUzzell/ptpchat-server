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
import argparse
import uuid

import signal

from ptpchat_server.util.config_manager import ConfigManager
from ptpchat_server.util.log_manager import LogManager

from ptpchat_server.net.comm_server import CommunicationServer
from ptpchat_server.net.message_handler import MessageHandler

from ptpchat_server.data.node_manager import NodeManager


logger_name = "ptpchat-server"
#file_name = '/var/log/ptpchat-server/ptpchat-server.log'

def setup(args, config):
    global listener, broadcast
    addr = (config.main.listen_host, config.main.listen_port)
    
    node_manager = NodeManager(config, LogManager(
        logger_name,
        file_name = config.main.log_file if args.log_to_file else None,
        module_name='node_manager', 
        log_level=config.main.node_log_level if args.log_level is None else args.log_level))
    
    threading.current_thread().name = "Main"
    
    message_handler = MessageHandler(LogManager(
        logger_name,
        file_name = config.main.log_file if args.log_to_file else None,
        module_name='message_handler',
        log_level=config.messages.log_level if args.log_level is None else args.log_level),
        node_manager)
    
    comms = CommunicationServer(config,
        LogManager(
            logger_name,
            file_name = config.main.log_file if args.log_to_file else None,
            module_name = "CommsServer", 
            log_level = config.communication.log_level if args.log_level is None else args.log_level), 
        node_manager, message_handler)
        
    #listener.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    comms_thread = threading.Thread(target=comms.serve_forever, name="Communication")
    comms_thread.daemon = True
    
    if not args.no_start:
        comms_thread.start()

    
def shutdown(signum, frame):
    global listener, broadcast, exit_flag
    threading.current_thread().name = "Main Shutdown"
    
    comms.shutdown()
    
    exit_flag.set()
    
def process_args(args):
    parser = argparse.ArgumentParser(description="ptpchat-server, main function. These arguments supersede any config file arguments")
    parser.add_argument('--log', dest='log_level', default=None, help="set a global log level")
    parser.add_argument('--no-log', dest='log_to_file', action='store_false', help="disable file logging")
    parser.add_argument('--no-start', dest='no_start', action='store_true', help="just setup and close")
    return parser.parse_args(args)
    
if __name__ == '__main__':

    args = process_args(sys.argv[1:])
    config = ConfigManager('/etc/ptpchat-server/server.cfg')
    setup(args, config)
    
    if args.no_start:
        quit()
        
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
