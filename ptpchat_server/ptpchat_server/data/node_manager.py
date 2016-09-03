
import threading
import re
import time
import operator
import logging

from ptpchat_server.base.node import Node
from ptpchat_server.util.read_monitor import ReadMonitor

logger = logging.getLogger(__name__)

class NodeManager:

    log_deleted_node = "NodeManager, deleted node: %s"
    log_add_node_already_exists = "NodeManager, tried to add node that already exists: %s"

    def __init__(self, config):

        if config is None:
            raise AttributeError("NodeManager Init, logger is None")

        self.node_cutoff = config.communication.node_cutoff

        self.monitor = ReadMonitor()

        self.nodes = {}

        self.local_node = Node(config.main.server_id,
            version = config.main.version,
            attributes = {Node.NODE_TYPE: Node.NODE_TYPE_SERVER}
        )

    def update_nodes(self):
        logger.debug("pruning node list")
        nodes = self.get_nodes({'last_seen_lt': time.time() - self.node_cutoff})

        if nodes is not None and len(nodes) > 0:
            for node in nodes:
                self.drop_node(node)

    '''
    An acceptable node is one where either:
        * Its TTL is one
        * Sent us a ROUTING message to the node (with the lowest TTL)
    '''
    def get_node_for_target(self, target_node):

        if target_node.seen_through is None:
            return target_node

        #nodes = self.get_nodes({Node.TTL : 1})

        #if nodes is None or len(nodes) == 0:
        #    return None

        #if target_node in nodes:
        #    return target_node

        #connecting_nodes = [(n, n.connections[target_node.base_id]) for n in nodes if node.connects_to(target_node)]

        nodes = self.get_nodes({Node.BASE_ID: target_node.seen_through})

        if len(nodes) != 0:
            return nodes[0]

        return None

    def add_node(self, node_data):

        if Node.NODE_ID not in node_data or not Node.is_valid_node_id(node_data[Node.NODE_ID]):
            raise AttributeError("NodeManager, invalid node_id in add_node")

        node = Node(node_data[Node.NODE_ID], node_data)

        if len(self.get_nodes(node_data)) > 0:
            logger.info(NodeManager.log_add_node_already_exists % node_data[Node.NODE_ID])
            return node

        self.monitor.start_write()
        self.nodes[node.base_id] = node
        self.monitor.end_write()

        return node

    def update_node(self, node):

        if node is None or not isinstance(node, Node):
            raise AttributeError("NodeManager, invalid node in update")

        self.monitor.start_read()

        if node.base_id not in self.nodes:
            self.monitor.end_read()
            raise AttributeError("NodeManager, updating node not in nodes!")

        self.monitor.end_read()
        self.monitor.start_write()
        self.nodes[node.base_id] = node
        self.monitor.end_write()

        return None

    def drop_node(self, node):

        if node is None or not isinstance(node, Node):
            raise AttributeError("NodeManager, invalid node in update")

        base_id = node.base_id

        self.monitor.start_read()
        if base_id not in self.nodes:
            self.monitor.end_read()
            raise AttributeError("NodeManager, node_id not found!")

        self.monitor.end_read()
        self.monitor.start_write()
        del self.nodes[base_id]
        self.monitor.end_write()
        logger.info(NodeManager.log_deleted_node % node.node_id)

    def get_channels(self):
        pass

    def get_nodes(self, args):

        self.monitor.start_read()
        if args is None:
            nodes = self.nodes.values()
        else:
            nodes = [self.nodes[x] for x in self.nodes if self.__matches(x, args)]
        self.monitor.end_read()
        return nodes

    # MUST have read lock!!!
    def __matches(self, node, args):
        return_node = None
        node = self.nodes[node]
        if Node.NODE_ID in args:
            return_node = node if args[Node.NODE_ID] == node.node_id else None
        if Node.BASE_ID in args:
            return_node = node if args[Node.BASE_ID] == node.base_id else None
        if Node.TTL in args:
            return_node = node if args[Node.TTL] == node.ttl else None
        if Node.SEEN_THROUGH in args:
            return_node = node if args[Node.SEEN_THROUGH] == node.seen_through else None
        if 'connected_to' in args:
            return_node = node if args['connected_to'] in node.connections else None
        if 'excluding_base_id' in args:
            return_node = node if args[Node.BASE_ID] != node.base_id else None
        if 'last_seen_lt' in args:
            return_node = node if args['last_seen_lt'] > node.last_seen else None
        if 'last_seen_gt' in args:
            return_node = node if args['last_seen_gt'] < node.last_seen else None
        return return_node is not None
