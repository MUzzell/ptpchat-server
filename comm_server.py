
from twisted.internet.protocol import Factory
from twisted.protocols.basic import Int32StringReceiver
from twisted.internet import reactor, protocol, task

from message_handler import MessageHandler

class MessageReceiver(Int32StringReceiver):

    def __init__(self, message_handler, addr):
        self.message_handler = message_handler
        self.addr = addr

    def connectionMade(self):
        self.factory.connectionAdded(self)
        
    def connectionLost(self, reason):
        self.factory.connectionRemoved(self)

    def stringReceived(self, string):
        self.message_handler.handle(string, self, self.factory)
        
class MessageFactory(Factory):

    log_connection_added = "Client connection added: %s"
    log_connection_removed = "Client connection removed; %s"
    
    def __init__(self, config, logger, node_manager, message_handler):
        self.logger = logger;
        self.node_manager = node_manager
        self.message_handler = message_handler
        self.clients = []
        
    def buildProtocol(self, addr):
        return MessageReceiver(self.message_handler, addr)
        
    def connectionAdded(self, client):
        self.logger.info(log_connection_added % client)
        self.clients.add(client)
        
    def connectionRemoved(self, client):
        self.logger.info(log_connection_removed % client)
        self.clients.remove(client)
        
    def broadcast(self):
        self.node_manager.update_nodes()
        self.broadcast_hello()
        self.broadcast_routing()
        
    def send_message(self, data, target_id):
        pass
        
    def send_messages(self, data, target_ids):
    
        if type(target_ids) is not list:
            raise AttributeError("MessageFactory, target_ids is not list")
        
        for target_id in target_ids:
            self.send_message(data, target_id)
        
    
class CommunicationServer():
    
    def __init__(self, config, logger, node_manager, message_handler):
       
        if logger is None or node_manager is None or config is None:
            raise AttributeError("ListenerServer Init, logger, config, or node_manager is None")
       
        self.server_address = (config.main.listen_host, config.main.listen_port)
        
        self.factory = MessageFactory(config, logger, node_manager, message_handler)
        
        reactor.listenTCP(config.main.listen_port, self.factory)
        
        self.broadcast_loop = task.LoopingCall(self.broadcast)
        
    def broadcast(self):
        self.factory.broadcast()
        
    def serve_forever(self):
        self.logger.info("ListenerServer starting up")
        self.logger.debug("Listening on: %s:%d" % self.server_address)
        self.broadcast_loop.start(10, now=False)
        reactor.run()
        
    def shutdown(self):
        self.logger.info("ListenerServer shutting down")
        self.broadcast_loop.stop()
        reactor.stop()
        
        