'''
'   ConnectHandler
'  
'   TODO: ipv6 matching
'   TODO: accepting CONNECTS to this server.
'   TODO: what if we cant find / talk to B?
'   TODO: you could probably DDoS with this, how to prevent / mitigate?
'   #TODO: verify packets came from the correct hosts
'''

from base_handler import BaseHandler
import time

import pdb, re


class ConnectHandler(BaseHandler):

    DST = 'dst'
    SRC = 'src'
    SRC_NODE_ID = 'src_node_id'
    DST_NODE_ID = 'dst_node_id'
    
    log_no_src = "CONNECT, no src in msg_data"
    log_no_dst = "CONNECT, no dst in msg_data"
    log_no_src_id = "CONNECT, no src_node_id in data"
    log_no_dst_id = "CONNECT, no dst_node_id in data"
    
    log_invalid_ids = "CONNECT, invalid node_id(s)"
    log_invalid_data = "CONNECT, invalid src and/or dst"
    
    log_could_not_find_nodes = "CONNECT, could not find node(s) with given node_id(s)!"
    
    
    ipv4_socket_match = "^((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))?\:?([0-9]{,5})?$"

    def __init__(self, uuid, logger= None, node_manager= None, extras = None):
        BaseHandler.__init__(self, uuid, logger, node_manager)
        self.verb = 'CONNECT'
        self.ipv4_socket_re = re.compile(ConnectHandler.ipv4_socket_match)
        
    def handleVerb(self, data, addr, sock):
    
        if ConnectHandler.SRC not in data:
            self.logger.warning(ConnectHandler.log_no_src)
            return
            
        if ConnectHandler.DST not in data:
            self.logger.warning(ConnectHandler.log_no_dst)
            return
            
        if ConnectHandler.SRC_NODE_ID not in data:
            self.logger.warning(ConnectHandler.log_no_src_id)
            return
            
        if ConnectHandler.DST_NODE_ID not in data:
            self.logger.warning(ConnectHandler.log_no_dst_id)
            return
            
        src_node_id = self.parse_uuid(data[ConnectHandler.SRC_NODE_ID])
        dst_node_id = self.parse_uuid(data[ConnectHandler.DST_NODE_ID])
        
        if src_node_id is None or dst_node_id is None:
            self.logger.warning(ConnectHandler.log_invalid_ids)
            return
            
        src = data[ConnectHandler.SRC]
        dst = data[ConnectHandler.DST]
        
        src_match = self.ipv4_socket_re.match(src)
        dst_match = self.ipv4_socket_re.match(dst)
        
        if src_match is None or dst_match is None:
            self.logger.warning(ConnectHandler.log_invalid_data)
            return
            
        src_match = src_match.groups()
        dst_match = dst_match.groups()
        
        if src_match == (None, None) or dst_match == (None, None):
            self.logger.warning(ConnectHandler.log_invalid_data)
            return
            
        if src_node_id == self.server_uuid or dst_node_id == self.server_uuid:
            self.logger.info("CONNECT, this msg is addressed to us!")
            return
            
        src_node = self.node_manager.get_nodes({BaseHander.NODE_ID : src_node_id})
        dst_node = self.node_manager.get_nodes({BaseHandler.NODE_ID : dst_node_id})
        
        if len(src_node) == 0 or len(dst_node) == 0:
            self.logger.warning(ConnectHandler.could_not_find_nodes)
            return #TODO; this is a genuine issue, must address
            
        src_node = src_node[0]
        dst_node = dst_node[0]
        
        #type 1: dst contains IP, src contains port. Add src IP and forward to dst node.
        if  ((dst_match[0] is not None and dst_match[1] is None) and 
                (src_match[0] is None and src_match[1] is not None)):
            self.send_message(self.build_message({
                ConnectHandler.SRC_NODE_ID : "%s" % src_node_id,
                ConnectHandler.DST_NODE_ID : "%s" % dst_node_id,
                ConnectHandler.SRC : "%s:%s" % (src_node[BaseHandler.CLIENT_ADDR][0], src_match[1]),
                ConnectHandler.DST : dst }), dst_node[BaseHandler.CLIENT_ADDR], sock)
           
        #type 2: dst contains full socket, src contains full socket. Forward to src node.
        if  ((dst_match[0] is not None and dst_match[1] is not None) and
                (src_match[0] is not None and src_match[1] is not None)):
            self.send_message(self.build_message({
                ConnectHandler.SRC_NODE_ID : "%s" % src_node_id,
                ConnectHandler.DST_NODE_ID : "%s" % dst_node_id,
                ConnectHandler.SRC : src,
                ConnectHandler.DST : dst }), src_node[BaseHandler.CLIENT_ADDR], sock)
            
        # if one of the other CONNECT messages, ignore
        return
            
            
    def buildMessage(self, data):
    
        #TODO, data check
    
        return self.compile_message(data)
            