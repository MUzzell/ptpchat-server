'''
message_handler.py

used by ListenerServer 


'''
import SocketServer, json, socket
import handlers import *

__handler_classes__ = {
    "HELLO" = hello_handler.HelloHandler
}

class MessageHandler(SocketServer.BaseRequestHandler):

    log_invalid_json = "ValueError, invalid json received"
    log_invalid_msg = "Invalid msg received, %s"
    log_invalid_verb = "Invalid verb received"
    
    MSG_TYPE = "msg_type"
    MSG_DATA = "msg_data"

    '''
    Important Note: A SocketServer will create a new instance of this 
    class for **each** request. therefore, the logger and other elements
    will need to be collected in this method, called once this is 
    instantiated.
    '''
    def setup(self):
        self.logger = self.server.logger
        self.node_manager = self.server.node_manager

    def handle(self):
        self.handle_request(self.request[0], self.client_address, self.request[1])
            
    
    def handle_request(self, data, addr, sock):
        try:
            msg = json.loads(data)
        except ValueError:
            self.logger.info(MessageHandler.log_invalid_json)
            return
            
        if type(msg) is not dict:
            self.logger.info(MessageHandler.log_invalid_msg % "not dictionary")
            return

        if MSG_TYPE not in msg or msg[MessageHandler.MSG_TYPE] is None:
            self.logger.info(MessageHandler.log_invalid_msg % "msg_type invalid")
        
        verb = msg[MessageHandler.MSG_TYPE].upper()
        data = msg[MessageHandler.MSG_DATA] if MSG_DATA in msg else None
        
        if data is None:
            self.logger.warning(MessageHandler.log_invalid_msg % "msg_data invalid")
        
        global __handler_classes__
        
        if verb not in __handler_classes__:
            self.logger.warning(MessageHandler.log_invalid_verb)
        
        handler = __handler_classes__[verb](self.logger, self.node_manager)
        handler.processData(data, addr, sock)
            
        return 0

    def handleVerb(self, data, addr):
        pass