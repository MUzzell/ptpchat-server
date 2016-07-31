
import logging
from twisted.internet.protocol import Factory
from twisted.protocols.basic import Int32StringReceiver
from twisted.internet import reactor, protocol, task
from twisted.python import log

from message_handler import MessageHandler
from ptpchat_server.base.node import Node
from ptpchat_server.handlers import BaseHandler

logger = logging.getLogger(__name__)

class MessageReceiver(Int32StringReceiver):

    def __init__(self, message_handler, addr, factory):
        self.message_handler = message_handler
        self.addr = addr
        self.node = None
        self.factory = factory

    def connectionMade(self):
        self.factory.connectionAdded(self)
        self.transport.setTcpKeepAlive(1)

    def connectionLost(self, reason):
        self.factory.connectionRemoved(self)

    def set_node(self, node):
        self.node = node
        #self.factory.attachNode(self,node);

    def stringReceived(self, string):
        if len(string) > 0:
            self.message_handler.handle(string, self, self.factory)

class MessageFactory(Factory):

    log_connection_added = "Client connection added: %s:%d"
    log_connection_removed = "Client connection removed; %s:%d"
    log_cannot_reach_node = "Unable to reach node: %s"

    def __init__(self, config, node_manager, message_handler):
        self.node_manager = node_manager
        self.message_handler = message_handler
        self.clients = []

    def buildProtocol(self, addr):
        return MessageReceiver(self.message_handler, addr, self)

    def connectionAdded(self, client):
        logger.info(MessageFactory.log_connection_added % (client.addr.host, client.addr.port))
        self.clients.append(client)
        self.send_hello(client)

    def connectionRemoved(self, client):
        logger.info(MessageFactory.log_connection_removed % (client.addr.host, client.addr.port))
        self.clients.remove(client)
        if client.node is None:
            return

        node = self.node_manager.get_nodes(client.node.base_id)[0]
        connecting_nodes = self.node_manager.get_nodes({'connected_to':node.base_id})
        connecting_nodes = [(x,connecting_nodes[x]) for x in connecting_nodes]
        connecting_nodes_ttl = sorted(connecting_nodes, key=lambda x: x[1].ttl)

        node.ttl = connecting_nodes_ttl[0][1]
        node.seen_through = connecting_nodes_ttl[0][0]

        self.node_manager.update_node(client.node)

    def send_hello(self, client):
        logger.debug("Sending HELLO to new connection: %s:%d" % (client.addr.host, client.addr.port))
        client.sendString(self.message_handler.buildHello())

    def sendRouting(self):
        msg = self.message_handler.buildRouting()

        for client in self.clients:
            client.sendString(msg)

    def send_message(self, data, target_node):
        node = self.node_manager.get_node_for_target(target_node)

        if node is None:
            logger.error(MessageFactory.log_cannot_reach_node % target_node)
            return

        clients = [x for x in self.clients if x.node == node]

        if clients is None or len(clients) == 0:
            logger.error(MessageFactory.log_cannot_reach_node % target_node)
            return

        clients[0].sendString(data)

    def send_messages(self, data, target_ids):

        if type(target_ids) is not list:
            raise AttributeError("MessageFactory, target_ids is not list")

        for target_id in target_ids:
            self.send_message(data, target_id)


class CommunicationServer:

    def __init__(self, config, logger, node_manager, message_handler):

        if logger is None or node_manager is None or config is None:
            raise AttributeError("CommunicationServer Init, logger, config, or node_manager is None")

        logger = logger
        self.observer = log.PythonLoggingObserver(loggerName='ptpchat-server')
        self.server_address = (config.main.listen_host, config.main.listen_port)

        self.process_nodes_interval = config.communication.process_nodes_interval
        self.broadcast_loop_interval = config.communication.broadcast_loop_interval

        self.factory = MessageFactory(config, logger, node_manager, message_handler)

        reactor.listenTCP(config.main.listen_port, self.factory)

        #self.broadcast_loop = task.LoopingCall(self.broadcast)

    def broadcast(self):
        self.factory.broadcast()

    def serve_forever(self):
        logger.info("CommunicationServer starting up")
        logger.debug("Listening on: %s:%d" % self.server_address)
        #self.broadcast_loop.start(self.broadcast_loop_interval, now=False)
        self.observer.start()
        reactor.run()
