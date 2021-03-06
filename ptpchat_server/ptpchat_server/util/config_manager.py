'''
# config_manager
#
'''

import ConfigParser
import os, pdb
import StringIO

class ConfigManager():

    main_section = "Main"
    communication_section = "Communication"
    messages_section = "Messages"

    defaults = StringIO.StringIO("""\
[Main]
server_name : testing
log_level : INFO
server_id : testing@5f715c17-4a41-482a-ab1f-45fa2cdd702b
listen_port : 9001
listen_host : 0.0.0.0
log_file : /var/log/ptpchat-server/server.log
log_to_file : True

[Communication]
broadcast_loop_interval : 2
node_cutoff : 15
process_nodes_interval : 30

[Messages]
log_level : INFO
""")

    main_section = "Main"
    listener_section = "Communication"
    broadcast_section = "Broadcast"

    def __init__(self, config_file=None):
        self.config = ConfigParser.RawConfigParser()

        if config_file is not None and os.path.exists(config_file):
            self.config.read(config_file)
        else:
            self.config.readfp(ConfigManager.defaults)

        self.messages = ConfigObject()
        self.communication = ConfigObject()
        self.main = ConfigObject()

        self.process_communication_config()
        self.process_messages_config()
        self.process_main_config()


    def process_communication_config(self):
        self.communication.broadcast_loop_interval = self.config.getint(ConfigManager.communication_section, "broadcast_loop_interval")
        self.communication.node_cutoff = self.config.getint(ConfigManager.communication_section, "node_cutoff")
        self.communication.process_nodes_interval = self.config.getint(ConfigManager.communication_section, "process_nodes_interval")

    def process_messages_config(self):
        self.messages.log_level = self.config.get(ConfigManager.messages_section, "log_level")

    def process_main_config(self):
        self.main.server_id = self.config.get(ConfigManager.main_section, "server_id")
        self.main.version = "ptpchat-server; 0.2"
        self.main.log_level = self.config.get(ConfigManager.main_section, "log_level")
        self.main.listen_port = self.config.getint(ConfigManager.main_section, "listen_port")
        self.main.listen_host = self.config.get(ConfigManager.main_section, "listen_host")
        self.main.log_file = self.config.get(ConfigManager.main_section, "log_file")
        self.main.log_to_file = self.config.getboolean(ConfigManager.main_section, "log_to_file")

class ConfigObject():
    pass
