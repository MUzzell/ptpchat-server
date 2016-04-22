'''
message_handler.py
used by ListenerServer 
'''
import json, socket, pdb

import ptpchat_server.handlers as handlers
from ptpchat_server.handlers.base_handler import BaseHandler
from ptpchat_server.base.node import Node

'''
Have you include the verb handler in handlers.__init__.py?
'''
__handler_classes__ = {
    "HELLO" : handlers.HelloHandler,
    "ROUTING" : handlers.RoutingHandler,
    #temporary additions for testing
    "CHANNEL" : BaseHandler,
    "MESSAGE" : BaseHandler
}

class MessageHandler():

    log_invalid_json = "ValueError, invalid json received"
    log_invalid_msg = "Invalid msg received, %s"
    log_invalid_verb = "Invalid verb received"
    log_msg_rejected = "%s message rejected"
    
    MSG_TYPE = "msg_type"
    MSG_DATA = "msg_data"

    def __init__(self, logger, node_manager):
        self.logger = logger
        self.node_manager = node_manager

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
            
        self.logger.debug("%s message received from %s:%d" % (verb, client.addr.host, client.addr.port))
        
        handler = __handler_classes__[verb](self.logger, self.node_manager)
        if not handler.handleMessage(msg, client, factory):
            self.logger.info(MessageHandler.log_msg_rejected % verb)
            
        return

    def broadcast_hello(self, factory):
    
        global __handler_classes__
        nodes = self.node_manager.get_nodes(None)
        self.logger.debug("Sending HELLO to %d nodes" % len(nodes))
        
        handler = __handler_classes__['HELLO'](self.logger, self.node_manager)
        for node in nodes:
            factory.send_message(handler.buildMessage(node), node)
        
    def broadcast_routing(self, factory):
    
        global __handler_classes__
        nodes = self.node_manager.get_nodes(None)
        self.logger.debug("Sending ROUTING to %d nodes" % len(nodes))
        
        handler = __handler_classes__['ROUTING'](self.logger, self.node_manager)
        for node in nodes:
            factory.send_message(handler.buildMessage(node), node)