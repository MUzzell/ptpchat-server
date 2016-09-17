
import unittest

import uuid
from collections import namedtuple

from ptpchat_server.data.node_graph import NodeGraph

class TestNodeGraph(unittest.TestCase):

    MainConfigTuple = namedtuple("main", ("server_id", "version"))
    CommunicationConfigTuple = namedtuple('communication',
        ("node_cutoff"))
    ConfigTuple = namedtuple("config", ("main", "communication"))

    def setUp(self):
        main_config = TestNodeGraph.MainConfigTuple(
            "test@710a82fc-26ae-4028-9972-5df373a01189", "TEST_CASE")
        comm_config = TestNodeGraph.CommunicationConfigTuple(
            60)
        config = TestNodeGraph.ConfigTuple(main_config, comm_config)

        self.manager = NodeGraph(config)


    def tearDown(self):
        pass

    def test_add_node_isStoredInNodes(self):
        node_uuid = uuid.uuid4().__str__()
        test_node_id = "testnode@{0}".format(node_uuid)
        node_data = {'node_id' : test_node_id }

        self.manager.add_node(node_data)

        # Not sure about this test
        self.assertIn(node_uuid, self.manager.nodes)

    def test_add_node_isStoredInGraph(self):
        node_uuid = uuid.uuid4().__str__()
        test_node_id = "testnode@{0}".format(node_uuid)
        node_data = {'node_id' : test_node_id }

        self.manager.add_node(node_data)
        # Not sure about this test
        self.assertIn(node_uuid, self.manager.graph)

    def test_add_node_rejectsEmptyCall(self):

        self.assertRaises(AttributeError, self.manager.add_node, None)

    def test_add_node_rejectsEmptyNodeData(self):
        self.assertRaises(AttributeError, self.manager.add_node, {})

    def test_add_node_rejectsInvalidNodeId(self):
        node_uuid = "00000000-0000-0000-0000-000000000000"
        test_node_id = "test"
        node_data = {'node_id' : test_node_id}

        self.assertRaises(AttributeError,self.manager.add_node, (node_data))

if __name__ == '__main__':
    unittest.main()