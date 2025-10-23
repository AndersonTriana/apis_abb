"""
Unit tests for Node class.

This module contains tests for the Node class including validation
of document constraints and data integrity.
"""

import pytest
from api_avl.model.node import Node


class TestNodeCreation:
    """Tests for Node creation and initialization."""

    def test_create_node_with_valid_document(self):
        """Test creating a node with valid document."""
        node = Node(
            document=123456,
            data={"document": 123456, "name": "Alice", "age": 10}
        )
        
        assert node.document == 123456
        assert node.data["name"] == "Alice"
        assert node.left is None
        assert node.right is None
        assert node.height == 1

    def test_create_node_with_string_document(self):
        """Test creating a node with string document (should convert to int)."""
        node = Node(
            document="12345",
            data={"document": "12345", "name": "Bob"}
        )
        
        assert node.document == 12345
        assert isinstance(node.document, int)

    def test_create_node_with_zero_document(self):
        """Test creating a node with document = 0."""
        node = Node(
            document=0,
            data={"document": 0, "name": "Zero"}
        )
        
        assert node.document == 0

    def test_create_node_with_max_valid_document(self):
        """Test creating a node with maximum valid document (999999)."""
        node = Node(
            document=999999,
            data={"document": 999999, "name": "Max"}
        )
        
        assert node.document == 999999


class TestNodeValidation:
    """Tests for Node validation rules."""

    def test_document_exceeds_six_digits_raises_error(self):
        """Test that document with more than 6 digits raises ValueError."""
        with pytest.raises(ValueError, match="max 6 digits"):
            Node(
                document=1000000,
                data={"document": 1000000, "name": "Invalid"}
            )

    def test_negative_document_raises_error(self):
        """Test that negative document raises ValueError."""
        with pytest.raises(ValueError, match="max 6 digits"):
            Node(
                document=-1,
                data={"document": -1, "name": "Invalid"}
            )

    def test_invalid_string_document_raises_error(self):
        """Test that non-numeric string document raises ValueError."""
        with pytest.raises(ValueError, match="cannot be converted"):
            Node(
                document="abc123",
                data={"document": "abc123", "name": "Invalid"}
            )

    def test_non_integer_document_raises_error(self):
        """Test that non-integer document type raises TypeError."""
        with pytest.raises(TypeError, match="must be an integer"):
            Node(
                document=12.5,  # type: ignore
                data={"document": 12.5, "name": "Invalid"}
            )


class TestNodeStructure:
    """Tests for Node structure and relationships."""

    def test_node_with_children(self):
        """Test creating a node with left and right children."""
        left_child = Node(document=10, data={"document": 10, "name": "Left"})
        right_child = Node(document=30, data={"document": 30, "name": "Right"})
        
        parent = Node(
            document=20,
            data={"document": 20, "name": "Parent"},
            left=left_child,
            right=right_child,
            height=2
        )
        
        assert parent.left == left_child
        assert parent.right == right_child
        assert parent.height == 2

    def test_node_height_default(self):
        """Test that default node height is 1."""
        node = Node(document=100, data={"document": 100, "name": "Test"})
        assert node.height == 1

    def test_node_data_integrity(self):
        """Test that node data is stored correctly."""
        data = {
            "document": 12345,
            "name": "Alice",
            "age": 10,
            "grade": "5th",
            "parent": {"name": "John", "phone": "555-1234"}
        }
        
        node = Node(document=12345, data=data)
        
        assert node.data == data
        assert node.data["name"] == "Alice"
        assert node.data["parent"]["name"] == "John"


class TestNodeEdgeCases:
    """Tests for edge cases in Node creation."""

    def test_document_boundary_lower(self):
        """Test document at lower boundary (0)."""
        node = Node(document=0, data={"document": 0, "name": "Zero"})
        assert node.document == 0

    def test_document_boundary_upper(self):
        """Test document at upper boundary (999999)."""
        node = Node(document=999999, data={"document": 999999, "name": "Max"})
        assert node.document == 999999

    def test_document_just_over_limit(self):
        """Test document just over the limit."""
        with pytest.raises(ValueError, match="max 6 digits"):
            Node(document=1000000, data={"document": 1000000, "name": "Over"})

    def test_string_document_with_leading_zeros(self):
        """Test string document with leading zeros."""
        node = Node(document="00123", data={"document": "00123", "name": "Test"})
        assert node.document == 123

    def test_empty_data_dictionary(self):
        """Test creating node with minimal data."""
        node = Node(document=100, data={"document": 100})
        assert node.document == 100
        assert "document" in node.data
