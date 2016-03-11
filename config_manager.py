'''
# config_manager
#
'''

import ConfigParser
import os, pdb
import StringIO

class ConfigManager():

    main_section = "Main"
    listener_section = "Listener"
    broadcast_section = "Broadcast"

    defaults = StringIO.StringIO("""\
[Main]
node_log_level : DEBUG
server_uuid : 5f715c17-4a41-482a-ab1f-45fa2cdd702b
listen_port : 9001
listen_host : 0.0.0.0
log_file : /var/log/ptpchat-server/server.log
log_to_file : True

[Listener]
log_level : INFO

[Broadcast]
log_level : INFO
loop_sleep : 2
node_cutoff : 15
process_nodes_interval : 30
""")
    
    main_section = "Main"
    listener_section = "Listener"
    broadcast_section = "Broadcast"

    def __init__(self, config_file=None):
        self.config = ConfigParser.RawConfigParser()
        pdb.set_trace()
        if config_file is not None and os.path.exists(config_file):
            self.config.read(config_file)
        else:
            self.config.readfp(ConfigManager.defaults)
            
        
        
        
        self.listener = ConfigObject()
        self.broadcast = ConfigObject()
        self.main = ConfigObject()
        
        self.process_listener_config()
        self.process_broadcast_config()
        self.process_main_config()
    
    
    def process_listener_config(self):
        self.listener.log_level  = self.config.get(ConfigManager.listener_section, "log_level")
    
    def process_broadcast_config(self):
        self.broadcast.log_level = self.config.get(ConfigManager.broadcast_section, "log_level")
        self.broadcast.loop_sleep = self.config.getint(ConfigManager.broadcast_section, "loop_sleep")
        self.broadcast.node_cutoff = self.config.getint(ConfigManager.broadcast_section, "node_cutoff")
        self.broadcast.process_nodes_interval = self.config.getint(ConfigManager.broadcast_section, "process_nodes_interval")
        
    def process_main_config(self):
        self.main.server_uuid = self.config.get(ConfigManager.main_section, "server_uuid")
        self.main.node_log_level = self.config.get(ConfigManager.main_section, "node_log_level")
        self.main.listen_port = self.config.getint(ConfigManager.main_section, "listen_port")
        self.main.listen_host = self.config.get(ConfigManager.main_section, "listen_host")
        self.main.log_file = self.config.get(ConfigManager.main_section, "log_file")
        self.main.log_to_file = self.config.getboolean(ConfigManager.main_section, "log_to_file")
    
class ConfigObject():
    pass
 