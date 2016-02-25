#!/usr/bin/python
#
# Experimental ptpchat-server (UDP)
# Very much wip
#
#
#

import pdb, os, datetime, sys
import socket
import json

UDP_IP = "0.0.0.0"
UDP_PORT = 9001

MSG_TYPE = 'msg_type'
MSG_DATA = 'msg_data'

msg_processors = {
'HELLO': process_hello(sock, x)
}

def process_hello(data):
    pass

def main_loop(ip, port):
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.bind((ip, port))
    
    while True:
        data, addr = sock.recvfrom(1024)
        pdb.settrace()
        
        process_message(sock, data, addr)
        
def process_message(sock, data, addr):
    try:
        msg = json.loads(data)
    except ValueError:
        return 1
        
    if type(msg) is not dict:
        return 1

    if MSG_TYPE not in msg || msg[MSG_TYPE] is None:
        return 1
    
    verb = msg[MSG_TYPE].upper()
    data = msg[MSG_DATA] if MSG_DATA in msg else None
    
    if verb not in msg_processors:
        return 1

    msg_processors[verb](sock, data)

    return 0

if __name__ == '__main__':
	main_loop(UDP_IP, UDP_PORT)