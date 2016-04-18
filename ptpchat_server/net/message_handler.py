'''
message_handler.py
used by ListenerServer 
'''
import json, socket
import handlers

from ptpchat_server.handlers.base_handler import BaseHandler
from ptpchat_server.base.node import Node

'''
Have you include the verb handler in handlers.__init__.py?
'''
__handler_classes__ = {
    "HELLO" : handlers.HelloHandler,
    "ROUTING" : handlers.RoutingHandler
}

class MessageHandler():

    log_invalid_json = "ValueError, invalid json received"
    log_invalid_msg = "Invalid msg received, %s"
    log_invalid_verb = "Invalid verb received"
    log_ttl_exceeded = "TTL value for message exceeded (<=0), ignoring"
    log_ttl_rebroadcast_exceeded = "TTL value for message broadcast exceeded"
    log_msg_rejected = "%s message rejected"
    log_flood_no_node_id = "Message to be flooded, but no node_id, ignoring"
    
    MSG_TYPE = "msg_type"
    MSG_DATA = "msg_data"

    '''
    Important Note: A SocketServer will create a new instance of this 
    class for **each** request. therefore, the logger and other elements
    will need to be collected in this method, called once this is 
    instantiated.
    '''
    def __init__(self, logger, node_manager):
        self.logger = self.server.logger
        self.node_manager = self.node_manager

    def handle(self, string, client, factory):
        try:
            self.handle_request(string, client, factory)
        except Exception as e:
            self.logger.error("Unhandled error in request: %s" % e.message)
    
    def handle_request(self, data, client, factory):
        self.logger.debug("Message handler, received message")
        try:
            msg = json.loads(data)
        except ValueError:
            self.logger.info(MessageHandler.log_invalid_json)
            return
            
        if type(msg) is not dict:
            self.logger.info(MessageHandler.log_invalid_msg % "not dictionary")
            return

        if MessageHandler.MSG_TYPE not in msg or msg[MessageHandler.MSG_TYPE] is None:
            self.logger.info(MessageHandler.log_invalid_msg % "msg_type invalid")
        
        verb = msg[MessageHandler.MSG_TYPE].upper()
         
        global __handler_classes__
        
        if verb not in __handler_classes__:
            self.logger.warning(MessageHandler.log_invalid_verb)
            return 
            
        self.logger.debug("%s message received from %s" % (verb, "%s:%d" % client))
        
        handler = __handler_classes__[verb](self.server_uuid, self.logger, self.node_manager)
        if not handler.handleMessage(data, client, factory):
            self.logger.info(MessageHandler.log_message_rejected % verb)
            return
            
        #TODO: handle relaying
            
        if not flood:
            return 0
            
        ttl = ttl - 1
        
        if ttl <= 0:
            self.logger.info(MessageHandler.log_ttl_rebroadcast_exceeded)
            
        if 'node_id' not in data:
            self.logger.info(log_flood_no_node_id)
            return 0
            
        #At this point, the node_id 'should' be verified.
        #OK, this has to be bad practice :S
        node_id = data[BaseHandler.NODE_ID]
        
        nodes = self.node_manager.getNodes({'excluding_node_id' : node_id})
        
        for node in nodes:
            handler.send_message(
                handler.build_message(data, ttl, flood),
                node[BaseHandler.CLIENT_ADDR], sock)

        return

    def broadcast_hello(self):
        
        nodes = self.node_manager.get_nodes(None)
        self.logger.debug("Sending HELLO to %d nodes" % len(nodes))
        
        for node in nodes:
            self.sock.sendto(self.handlers['HELLO'].buildMessage(node), node['client_client'])
        
    def broadcast_routing(self):
        nodes = self.node_manager.get_nodes(None)
        self.logger.debug("Sending ROUTING to %d nodes" % len(nodes))
        for node in nodes:
            self.sock.sendto(self.handlers['ROUTING'].buildMessage(node), node['client_client'])