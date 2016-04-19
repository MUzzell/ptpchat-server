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
    global comms
    addr = (config.main.listen_host, config.main.listen_port)
    
    logger = LogManager(
        logger_name,
        file_name = config.main.log_file if args.log_to_file else None,
        log_level=config.main.node_log_level if args.log_level is None else args.log_level)
    
    node_manager = NodeManager(config, logger)
    
    message_handler = MessageHandler(logger, node_manager)
    
    comms = CommunicationServer(config, logger, node_manager, message_handler)
        
    #listener.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    
    if not args.no_start:
        comms.serve_forever()

    
def shutdown(signum, frame):
    global comms, exit_flag
    comms.shutdown()
    
    exit_flag.set()
    
def process_args(args):
    parser = argparse.ArgumentParser(description="ptpchat-server, main function. These arguments supersede any config file arguments")
    parser.add_argument('--log', dest='log_level', default=None, help="set a global log level")
    parser.add_argument('--no-log', dest='log_to_file', action='store_false', help="disable file logging")
    parser.add_argument('--no-start', dest='no_start', action='store_true', default=False, help="just setup and close")
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
