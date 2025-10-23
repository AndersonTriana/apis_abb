"""
Unit tests for the Node class.
"""
import pytest
from api_abb.model.node import Node


class TestNode:
    """Test suite for Node class."""
    
    def test_node_creation_with_id_only(self):
        """Test creating a node with only an id."""
        node = Node(id=10)
        
        assert node.id == 10
        assert node.data is None
        assert node.left is None
        assert node.right is None
    
    def test_node_creation_with_id_and_data(self):
        """Test creating a node with id and data."""
        node = Node(id=5, data="test data")
        
        assert node.id == 5
        assert node.data == "test data"
        assert node.left is None
        assert node.right is None
    
    def test_node_with_various_data_types(self):
        """Test node with different data types."""
        # String data
        node1 = Node(id=1, data="string")
        assert node1.data == "string"
        
        # Integer data
        node2 = Node(id=2, data=100)
        assert node2.data == 100
        
        # Dictionary data
        node3 = Node(id=3, data={"key": "value"})
        assert node3.data == {"key": "value"}
        
        # List data
        node4 = Node(id=4, data=[1, 2, 3])
        assert node4.data == [1, 2, 3]
    
    def test_node_left_and_right_assignment(self):
        """Test assigning left and right children."""
        parent = Node(id=10, data="parent")
        left_child = Node(id=5, data="left")
        right_child = Node(id=15, data="right")
        
        parent.left = left_child
        parent.right = right_child
        
        assert parent.left == left_child
        assert parent.right == right_child
        assert parent.left.id == 5
        assert parent.right.id == 15
    
    def test_node_repr(self):
        """Test string representation of node."""
        node = Node(id=42, data="answer")
        repr_str = repr(node)
        
        assert "Node" in repr_str
        assert "42" in repr_str
        assert "answer" in repr_str
    
    def test_node_to_dict(self):
        """Test converting node to dictionary."""
        node = Node(id=7, data="test")
        node_dict = node.to_dict()
        
        assert isinstance(node_dict, dict)
        assert node_dict["id"] == 7
        assert node_dict["data"] == "test"
        assert "left" not in node_dict
        assert "right" not in node_dict
    
    def test_node_to_dict_with_none_data(self):
        """Test to_dict with None data."""
        node = Node(id=99)
        node_dict = node.to_dict()
        
        assert node_dict["id"] == 99
        assert node_dict["data"] is None
