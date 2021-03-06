
import json
from uuid import UUID, uuid4

from ptpchat_server.base.node import Node
from . import exceptions

class BaseHandler:

    log_invalid_node_id = "Received node id in sender or target is invalid, ignoring"
    log_invalid_msg_id = "Received msg_id is invalid, ignoring"
    log_ttl_exceeded = "TTL value for message exceeded (<=0), ignoring"
    log_ttl_rebroadcast_exceeded = "TTL value for message broadcast exceeded"
    log_msg_rejected = "%s message rejected"
    log_flood_no_node_id = "Message to be flooded, but no node_id, ignoring"
    log_invalid_sender_id = "Invalid 'sender_id', ignoring"

    MSG_TYPE = 'msg_type'
    MSG_DATA = 'msg_data'

    LAST_SEEN = 'last_seen'

    SENDER_ID = 'sender_id'
    TARGET_ID = 'target_id'

    MSG_ID = 'msg_id'

    TTL = 'ttl'
    FLOOD = 'flood'

    def __init__(self, logger=None, node_manager=None):
        self.verb = None
        self.ttl = 1
        self.flood = False
        self.logger = logger
        self.node_manager = node_manager

    def handle_message(self, msg, client, factory):

        data = msg[BaseHandler.MSG_DATA] if BaseHandler.MSG_DATA in msg else None

        if data is None or type(data) is not dict:
            raise exceptions.InvalidMessage("msg_data")

        ttl = msg[BaseHandler.TTL] if BaseHandler.TTL in msg else None
        flood = msg[BaseHandler.FLOOD] if BaseHandler.FLOOD in msg else None
        msg_id = msg[BaseHandler.MSG_ID] if BaseHandler.MSG_ID in msg else None

        if ttl is None or type(ttl) is not int:
            raise exceptions.InvalidMessage("ttl")

        if ttl <= 0:
            raise exceptions.TtlExceeded(None, None) # Do nothing

        if flood is None or type(flood) is not bool:
            raise exceptions.InvalidMessage("flood")

        if msg_id is None or self.parse_uuid(msg_id) is None:
            raise exceptions.InvalidMessagE("msg_id")

        sender_id = msg[BaseHandler.SENDER_ID] if BaseHandler.SENDER_ID in msg else None
        target_id = msg[BaseHandler.TARGET_ID] if BaseHandler.TARGET_ID in msg else None

        if sender_id is None or not Node.is_valid_node_id(sender_id):
            raise exceptions.InvalidMessage("sender_id")

        if sender_id == self.node_manager.local_node.node_id:
            raise excpetions.InvalidMessage("sender_id")

        if target_id is not None and not Node.is_valid_node_id(target_id):
            raise exceptions.InvalidMessage("target_id")

        if target_id is None and not flood and ttl == 1:  # for this node
            return self.handle_verb(sender_id, data, client, factory)

        if target_id is not None and target_id == self.node_manager.local_node.node_id:
            return self.handle_verb(sender_id, data, client, factory)

        ttl -= 1

        if ttl <= 0:
            # TODO: send NACK
            raise exceptions.TtlExceeded(sender_id, msg_id)

        msg[BaseHandler.TTL] = ttl
        new_msg = json.dumps(msg)

        if flood:
            nodes = self.node_manager.get_nodes({'excluding_node_id': sender_id})
            factory.send_messages(new_msg, [x[BaseHandler.NODE_ID] for x in nodes])
        elif target_id is not None:
            factory.send_message(new_msg, target_id)

    def handle_verb(self, data, client, factory):
        self.logger.error("BaseHandler.handleVerb called!")
        raise Exception("BaseHandler.handle_verb called!")

    def build_message(self, data, target_id=None, ttl=None, flood=None):
        self.logger.error("BaseHandler.buildVerb called!")
        raise Exception("BaseHandler.build_verb called!")

    def parse_uuid(self, uid):
        try:
            val = UUID(uid, version=4)
        except ValueError:
            self.logger.debug("given uid incorrect, %s" % ValueError)
            return None
        return val

    def send_message(self, msg, client, sock):
        self.logger.debug("%s, Sending message to %s:%d" % self.verb, client[0], client[1])

        sock.sendto(msg, client)

    def compile_message(self, data, target_id = None, ttl=None, flood=None):
        if ttl is None:
            ttl = self.ttl
        if flood is None:
            flood = self.flood
        return json.dumps({
            BaseHandler.MSG_ID: "%s" % uuid4(),
            BaseHandler.TTL: ttl,
            BaseHandler.FLOOD: flood,
            BaseHandler.SENDER_ID: self.node_manager.local_node.node_id,
            BaseHandler.TARGET_ID: target_id,
            BaseHandler.MSG_TYPE: self.verb,
            BaseHandler.MSG_DATA: data})