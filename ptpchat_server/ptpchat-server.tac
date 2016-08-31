import logging
from twisted.web import server, resource
from twisted.python import log
from twisted.python.log import ILogObserver
from twisted.application import service
from twisted.application import internet
from twisted.internet import reactor

from ptpchat_server.util.config_manager import ConfigManager
from ptpchat_server.net.message_handler import MessageHandler
from ptpchat_server.net.comm_server import MessageFactory
from ptpchat_server.data.node_manager import NodeManager

config = ConfigManager('/etc/ptpchat-server/server.cfg')

logging_level = {
        "CRITICAL" : 50,
        "ERROR" : 40,
        "WARNING" : 30,
        "INFO" : 20,
        "DEBUG" : 10,
        "NOTSET" : 0
    }

logging.basicConfig(
	filename = config.main.log_file,
	filemode = 'a',
	level = logging_level[config.main.log_level],
	format = "%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger()

application = service.Application('twisted-ptpchat-server.tac')
application.setComponent(ILogObserver, log.PythonLoggingObserver().emit)

node_manager = NodeManager(config)
message_handler = MessageHandler(node_manager)

message_factory = MessageFactory(config, node_manager, message_handler)

internet.TCPServer(config.main.listen_port, message_factory).setServiceParent(application)