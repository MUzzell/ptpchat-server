
import re

class Node():

    NODE_ID = 'node_id'
    BASE_ID = 'base_id'
    NAME = 'name'
    ATTRIBUTES = 'attributes'
    VERSION = 'version'
    
    CLIENT_ADDR = 'client_client'
    LAST_SEEN = 'last_seen'
    
    TTL = 'ttl'
    
    NODE_TYPE = 'node_type'
    NODE_TYPE_SERVER = 'server'
    NODE_TYPE_CLIENT = 'client'
    
    node_id_pattern ="^([a-zA-Z0-9]+)@([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})$"
    
    node_id_regex = re.compile(node_id_pattern)
    
    @staticmethod
    def is_valid_node_id(node_id):
        if node_id is None or type(node_id) is not str:
            return False
        return Node.node_id_regex.match(node_id) is not None
    
    @staticmethod
    def parse_node_id(node_id):
        match = Node.node_id_regex.match(node_id)
        if match is None:
            raise AttributeError("NodeManager, Invalid NodeId")
        return match.groups()
    
    def __init__(self, node_id, node_data = None):
        if not Node.is_valid_node_id(node_id):
            raise AttributeError("Node, Invalid NodeId")
            
        self.node_id = node_id
        node_id_parts = Node.parse_node_id(node_id)
        self.name = node_id_parts[0]
        self.base_id = node_id_parts[1]
        
        if node_data is None:
            return
            
        self.connections = []
        self.version = node_data[Node.VERSION] if Node.VERSION in node_data else None
        self.last_seen = node_data[Node.LAST_SEEN] if Node.LAST_SEEN in node_data else None
        self.ttl = node_data[Node.TTL] if Node.TTL in node_data else 32 #default TTL
        
        attrs = node_data[Node.ATTRIBUTES] if Node.ATTRIBUTES in node_data else None
        
        
        if attrs is None:
            return
        
        if type(attrs) is not dict:
            raise AttributeError("Node, given 'attributes' is invalid")
        
        self.attributes = attrs        
        self.node_type = attrs[Node.NODE_TYPE] if Node.NODE_TYPE in attrs else None
        
    def connects_to(self, node):
        return len([n for n in self.connections if n == node]) > 0
        
    def __eq__(self, other):
        return self.base_id == other.base_id