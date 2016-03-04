#!/usr/bin/python
#
# Experimental ptpchat-server (UDP)
# Very much wip
#
# TODO: Most verbs, a timeout on known_ips, threading.
#

import pdb, os, datetime, sys
import socket
import json

UDP_IP = "0.0.0.0"
UDP_PORT = 9001

MSG_TYPE = 'msg_type'
MSG_DATA = 'msg_data'

global known_ips = []

base_routing_msg = {
    MSG_TYPE:'ROUTING', 
        MSG_DATA: {
            'users': [ ]}
    }

def process_hello(sock, addr, data):
    global known_ips
    if data is None:
        return
        
    if type(data) is not dict:
        return
        
    if data['username'] is None or data['username'] is "":
        return

    if addr not in known_ips:
        known_ips += [{'username': data['username'], 'address': "%s:%d" % addr}]
    
    sock.sendto(build_routing_msg(), addr)
    sock.close()

def process_routing(sock, addr, data):
    pass
    
def build_routing_msg():
    msg = base_routing_msg
    msg[MSG_DATA]['users'] = [{'username': x['username'], 'address':x['address']} for x in known_ips]
    return msg

msg_processors = {
'HELLO': lambda sock, addr, data: process_hello(sock, addr, data),
'ROUTING': lambda sock, addr, data: process_routing(sock, addr, data)
}

def main_loop(ip, port):
    print "in main loop"
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print "starting up"
    while True:
        data, addr = sock.recvfrom(1024)
        pdb.set_trace()
        
        process_message(sock, data, addr)
    print "connection close"
    conn.close()
        
def process_message(sock, data, addr):
    try:
        msg = json.loads(data)
    except ValueError:
        return 1
        
    if type(msg) is not dict:
        return 1

    if MSG_TYPE not in msg or msg[MSG_TYPE] is None:
        return 1
    
    verb = msg[MSG_TYPE].upper()
    data = msg[MSG_DATA] if MSG_DATA in msg else None
    
    if verb not in msg_processors:
        return 1

    msg_processors[verb](sock, addr, data)

    return 0

if __name__ == '__main__':
	main_loop(UDP_IP, UDP_PORT)
