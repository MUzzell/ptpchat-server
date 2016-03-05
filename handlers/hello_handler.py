
from base_handler import BaseHandler

class HelloHandler(BaseHandler):
    
    def handleVerb(self, data, addr, sock):
        self.logger.debug("Hello handler called")