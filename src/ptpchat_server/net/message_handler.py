'''
message_handler.py
used by ListenerServer
'''

import json
import socket
import pdb
import logging

import ptpchat_server.handlers as handlers
from ptpchat_server.handlers.base_handler import BaseHandler
from ptpchat_server.base.node import Node

logger = logging.getLogger(__name__)

class MessageHandler:

    log_invalid_json = "ValueError, invalid json received"
    log_invalid_msg = "Invalid msg received, %s"
    log_invalid_verb = "Invalid verb received"
    log_msg_rejected = "%s message rejected"

    MSG_TYPE = "msg_type"
    MSG_DATA = "msg_data"

    '''
    Have you include the verb handler in handlers.__init__.py?
    '''
    handler_classes = {
        "HELLO": handlers.HelloHandler,
        "ROUTING": handlers.RoutingHandler,
        # temporary additions for testing
        "CHANNEL": BaseHandler,
        "MESSAGE": BaseHandler
    }

    def __init__(self, node_manager):
        self.node_manager = node_manager

    def handle(self, string, client, factory):
        try:
            self.handle_request(string, client, factory)
        except Exception as e:
            logger.error("Unhandled error in request: %s" % e.message)

    def handle_request(self, data, client, factory):
        logger.debug("Message handler, received message")
        try:
            msg = json.loads(data)
        except ValueError:
            logger.info(MessageHandler.log_invalid_json)
            return

        if type(msg) is not dict:
            logger.info(MessageHandler.log_invalid_msg % "not dictionary")
            return

        if MessageHandler.MSG_TYPE not in msg or msg[MessageHandler.MSG_TYPE] is None:
            logger.info(MessageHandler.log_invalid_msg % "msg_type invalid")

        verb = msg[MessageHandler.MSG_TYPE].upper()

        if verb not in MessageHandler.handler_classes:
            logger.warning(MessageHandler.log_invalid_verb)
            return

        logger.debug("%s message received from %s:%d" % (verb, client.addr.host, client.addr.port))

        handler = MessageHandler.handler_classes[verb](logger, self.node_manager)
        if not handler.handleMessage(msg, client, factory):
            logger.info(MessageHandler.log_msg_rejected % verb)

        return

    def build_hello(self):
        handler = MessageHandler.handler_classes['HELLO'](logger, self.node_manager)
        return handler.buildMessage(None)

    def build_routing(self):
        handler = MessageHandler.handler_classes['ROUTING'](logger, self.node_manager)
        return handler.buildMessage(None)