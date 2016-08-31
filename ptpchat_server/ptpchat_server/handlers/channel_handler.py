
from base_handler import BaseHandler
import time

import pdb


class ChannelHandler(BaseHandler):

    log_no_node_id = "CHANNEL, no 'node_id' in data, ignoring"
    log_no_msg_id = "CHANNEL, no 'msg_id' in data, ignoring"
    log_node_id_invalid = "CHANNEL, invalid 'node_id', ignoring"
    log_msg_id_invalid = "CHANNEL, invalid 'msg_id', ignoring"
    log_node_id_same_as_server = "CHANNEL, invalid 'node_id', ignoring"

    log_adding_node = "CHANNEL, adding node: %s"
    log_updating_node = "CHANNEL, updating node: %s"

    def __init__(self, uuid, logger=None, node_manager=None, extras=None):
        BaseHandler.__init__(self, uuid, logger, node_manager)
        self.verb = 'CHANNEL'
        self.ttl = 32
        self.flood = True

    def handle_verb(self, data, addr, sock):

        if BaseHandler.NODE_ID not in data:
            self.logger.warning(ChannelHandler.log_no_node_id)
            return False

        node_id = self.parse_uuid(data[BaseHandler.NODE_ID])

        if node_id is None:
            self.logger.warning(ChannelHandler.log_node_id_invalid)
            return False

        if BaseHandler.MSG_ID not in data:
            self.logger.warning(ChannelHandler.log_no_node_id)
            return False

        msg_id = self.parse_uuid(data[BaseHandler.MSG_ID])

        if msg_id is None:
            self.logger.warning(ChannelHandler.log_msg_id_invalid)
            return False

        if node_id == self.server_uuid:
            self.logger.warning(ChannelHandler.log_node_id_same_as_server)
            return False

        # This server simply relays channel messages, so just add this node if necessary
        node = self.node_manager.get_nodes({BaseHandler.NODE_ID: node_id})

        if node is None or len(node) == 0:
            self.logger.info(ChannelHandler.log_adding_node % node_id)
            self.node_manager.add_node(
                {
                    BaseHandler.NODE_ID: node_id,
                    BaseHandler.CLIENT_ADDR: addr,
                    BaseHandler.LAST_SEEN: time.time()
                }
            )
        else:
            self.logger.info(ChannelHandler.log_updating_node % node_id)
            node = node[0]
            node['last_seen'] = time.time()
            self.node_manager.update_node(node)

        return True;

    def build_message(self, data, ttl=None, flood=None):

        return self.compile_message({
            BaseHandler.NODE_ID: "%s" % self.server_uuid,
            ChannelHandler.VERSION: self.version}, ttl, flood)

