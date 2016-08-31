import re


class Node:

    NODE_ID = 'node_id'
    BASE_ID = 'base_id'
    NAME = 'name'
    ATTRIBUTES = 'attributes'
    VERSION = 'version'

    CLIENT_ADDR = 'client_client'
    LAST_SEEN = 'last_seen'
    SEEN_THROUGH = 'seen_through'

    TTL = 'ttl'

    NODE_TYPE = 'node_type'
    NODE_TYPE_SERVER = 'server'
    NODE_TYPE_CLIENT = 'client'

    node_id_pattern ="^([a-zA-Z0-9]+)@([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})$"

    node_id_regex = re.compile(node_id_pattern)

    @staticmethod
    def is_valid_node_id(node_id):
        if node_id is None:
            return False
        return Node.node_id_regex.match(node_id) is not None

    @staticmethod
    def parse_node_id(node_id):
        match = Node.node_id_regex.match(node_id)
        if match is None:
            raise AttributeError("NodeManager, Invalid NodeId")
        return match.groups()

    def __init__(self, node_id, **kwargs):
        if not Node.is_valid_node_id(node_id):
            raise AttributeError("Node, Invalid NodeId")

        self.node_id = node_id
        node_id_parts = Node.parse_node_id(node_id)
        self.name = node_id_parts[0]
        self.base_id = node_id_parts[1]

        self.connections = {}
        self.version = getattr(kwargs, Node.VERSION, None)
        self.last_seen = getattr(kwargs, Node.LAST_SEEN, None)
        self.ttl = getattr(kwargs, Node.TTL, 32) # default TTL
        self.seen_through = getattr(kwargs, Node.SEEN_THROUGH, None)

        attrs = getattr(kwargs, Node.ATTRIBUTES, None)

        if attrs is None:
            return

        if type(attrs) is not dict:
            raise AttributeError("Node, given 'attributes' is invalid")

        self.attributes = attrs
        self.node_type = attrs[Node.NODE_TYPE] if Node.NODE_TYPE in attrs else None

    def connects_to(self, node):
        return len([n for n in self.connections if n == node.base_id]) > 0

    def __eq__(self, other):
        if type(other) is not Node:
            return False
        return self.base_id == other.base_id

    def __str__(self):
        return self.node_id
