import threading
import re
import time
import operator
import logging

from ptpchat_server.base.node import Node
from ptpchat_server.util.read_monitor import ReadMonitor

logger = logging.getName(__name__)

class NodeGraph:

    def __init__(self, config):

        if config is None:
            raise AttributeError("config is None")

        self.node_cutoff = config.communication.node_cutoff

        self.monitor = ReadMonitor()

        self.nodes = {}
        self.graph = {}

        self.local_node = Node(config.main.server_id,
            version = config.main.version,
            attributes = {Node.NODE_TYPE: Node.NODE_TYPE_SERVER}
        )

        self.graph[self.local_node.base_id] = []

    def add_node(self, node_data):

        if Node.NODE_ID not in node_data or not Node.is_valid_node_id(node_data[Node.NODE_ID]):
            raise AttributeError("invalid node_id")

        node = Node(node_data[Node.NODE_ID], node_data)

        if len(self.get_nodes(node_data)) > 0:
            logger.info(NodeManager.log_add_node_already_exists % node_data[Node.NODE_ID])
            return node

        with self.monitor.write():
            self.nodes[node.base_id] = node
            self.graph[node.base_id] = []

        return node

    def update_node(self, node):

        if node is None or not isinstance(node, Node):
            raise AttributeError("invalid node")

        with self.monitor.read():
            if node.base_id not in self.nodes:
                raise AttributeError("node not found")

        with self.monitor.write():
            self.nodes[node.base_id] = node

        return node

    def update_node_links(self, node, connections):

        if node is None or not isinstance(node, Node):
            raise AttributeError("invalid node")

        with self.monitor.write():
            if node.base_id not in self.nodes:
                raise AttributeError("node not found")

            self.graph[node.base_id] = _build_node_links(
                self.graph[node.base_id], connections)

    def _build_node_links(self, current, new):

        def get_key(item):
            return item[0]

        return list(set(current + new))

    def drop_node(self, node):

        if node is None or not isinstance(node, Node):
            raise AttributeError("invalid node")

        base_id = node.base_id

        with self.monitor.read():
            if base_id not in self.nodes:
                raise AttributeError("node not found")
            # it has to be in graph. it has to be!

        with self.monitor.write():
            del self.nodes[base_id]
            del self.graph[base_id]

        logger.info(NodeManager.log_deleted_node % node.node_id)