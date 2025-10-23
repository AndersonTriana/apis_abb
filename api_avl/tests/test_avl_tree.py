"""
Unit tests for AVL Tree implementation.

This module contains comprehensive tests for all AVL Tree methods including
insertion, deletion, search, traversals, and rotation validations.
"""

import pytest
from typing import List, Optional
from api_avl.model.avl_tree import AVLTree
from api_avl.model.node import Node


class TestAVLTreeBasicOperations:
    """Tests for basic AVL Tree operations."""

    def test_empty_tree_initialization(self):
        """Test that a new tree is empty."""
        tree = AVLTree()
        assert tree.size() == 0
        assert tree.is_empty() is True
        assert tree.get_root() is None

    def test_insert_single_node(self):
        """Test inserting a single node."""
        tree = AVLTree()
        child = {"document": 100, "name": "Alice"}
        tree.insert(child)
        
        assert tree.size() == 1
        assert tree.is_empty() is False
        assert tree.get_root() == child

    def test_insert_multiple_nodes_and_validate_size(self):
        """Test inserting multiple nodes and validating size."""
        tree = AVLTree()
        children = [
            {"document": 50, "name": "Alice"},
            {"document": 30, "name": "Bob"},
            {"document": 70, "name": "Charlie"},
            {"document": 20, "name": "David"},
            {"document": 40, "name": "Eve"},
        ]
        
        for child in children:
            tree.insert(child)
        
        assert tree.size() == 5
        assert len(tree) == 5

    def test_insert_duplicate_document_raises_error(self):
        """Test that inserting duplicate document raises ValueError."""
        tree = AVLTree()
        child = {"document": 100, "name": "Alice"}
        tree.insert(child)
        
        with pytest.raises(ValueError, match="already exists"):
            tree.insert({"document": 100, "name": "Bob"})

    def test_insert_without_document_key_raises_error(self):
        """Test that inserting without document key raises KeyError."""
        tree = AVLTree()
        
        with pytest.raises(KeyError, match="document"):
            tree.insert({"name": "Alice"})

    def test_insert_document_as_string(self):
        """Test inserting document as string (should convert to int)."""
        tree = AVLTree()
        child = {"document": "123", "name": "Alice"}
        tree.insert(child)
        
        assert tree.size() == 1
        result = tree.search(123)
        assert result is not None
        assert result["name"] == "Alice"

    def test_insert_document_exceeds_six_digits_raises_error(self):
        """Test that document with more than 6 digits raises ValueError."""
        tree = AVLTree()
        
        with pytest.raises(ValueError, match="max 6 digits"):
            tree.insert({"document": 1000000, "name": "Alice"})

    def test_insert_negative_document_raises_error(self):
        """Test that negative document raises ValueError."""
        tree = AVLTree()
        
        with pytest.raises(ValueError, match="max 6 digits"):
            tree.insert({"document": -1, "name": "Alice"})


class TestAVLTreeSearch:
    """Tests for search operations."""

    def test_search_existing_node(self):
        """Test searching for an existing node."""
        tree = AVLTree()
        children = [
            {"document": 50, "name": "Alice"},
            {"document": 30, "name": "Bob"},
            {"document": 70, "name": "Charlie"},
        ]
        
        for child in children:
            tree.insert(child)
        
        result = tree.search(30)
        assert result is not None
        assert result["name"] == "Bob"
        assert result["document"] == 30

    def test_search_non_existing_node(self):
        """Test searching for a non-existing node."""
        tree = AVLTree()
        tree.insert({"document": 50, "name": "Alice"})
        
        result = tree.search(100)
        assert result is None

    def test_search_in_empty_tree(self):
        """Test searching in an empty tree."""
        tree = AVLTree()
        result = tree.search(50)
        assert result is None

    def test_search_with_string_document(self):
        """Test searching with string document."""
        tree = AVLTree()
        tree.insert({"document": 50, "name": "Alice"})
        
        result = tree.search("50")
        assert result is not None
        assert result["name"] == "Alice"

    def test_contains_operator(self):
        """Test using 'in' operator for search."""
        tree = AVLTree()
        tree.insert({"document": 50, "name": "Alice"})
        
        assert 50 in tree
        assert 100 not in tree


class TestAVLTreeRotations:
    """Tests for AVL Tree rotation operations."""

    def test_insert_left_rotation(self):
        """Test simple left rotation (Right-Right case)."""
        tree = AVLTree()
        # Insert in ascending order to trigger left rotation
        tree.insert({"document": 10, "name": "A"})
        tree.insert({"document": 20, "name": "B"})
        tree.insert({"document": 30, "name": "C"})
        
        # After left rotation, root should be 20
        root = tree.get_root()
        assert root["document"] == 20
        
        # Verify tree structure
        in_order = tree.in_order()
        assert [node["document"] for node in in_order] == [10, 20, 30]

    def test_insert_right_rotation(self):
        """Test simple right rotation (Left-Left case)."""
        tree = AVLTree()
        # Insert in descending order to trigger right rotation
        tree.insert({"document": 30, "name": "C"})
        tree.insert({"document": 20, "name": "B"})
        tree.insert({"document": 10, "name": "A"})
        
        # After right rotation, root should be 20
        root = tree.get_root()
        assert root["document"] == 20
        
        # Verify tree structure
        in_order = tree.in_order()
        assert [node["document"] for node in in_order] == [10, 20, 30]

    def test_insert_left_right_rotation(self):
        """Test double rotation: left-right (Left-Right case)."""
        tree = AVLTree()
        tree.insert({"document": 30, "name": "C"})
        tree.insert({"document": 10, "name": "A"})
        tree.insert({"document": 20, "name": "B"})
        
        # After left-right rotation, root should be 20
        root = tree.get_root()
        assert root["document"] == 20
        
        # Verify tree structure
        in_order = tree.in_order()
        assert [node["document"] for node in in_order] == [10, 20, 30]

    def test_insert_right_left_rotation(self):
        """Test double rotation: right-left (Right-Left case)."""
        tree = AVLTree()
        tree.insert({"document": 10, "name": "A"})
        tree.insert({"document": 30, "name": "C"})
        tree.insert({"document": 20, "name": "B"})
        
        # After right-left rotation, root should be 20
        root = tree.get_root()
        assert root["document"] == 20
        
        # Verify tree structure
        in_order = tree.in_order()
        assert [node["document"] for node in in_order] == [10, 20, 30]

    def test_complex_rotations_sequence(self):
        """Test multiple rotations in a complex insertion sequence."""
        tree = AVLTree()
        documents = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 55]
        
        for doc in documents:
            tree.insert({"document": doc, "name": f"Person{doc}"})
        
        # Verify tree is balanced
        assert tree.size() == len(documents)
        
        # Verify in-order traversal is sorted
        in_order = tree.in_order()
        in_order_docs = [node["document"] for node in in_order]
        assert in_order_docs == sorted(documents)
        
        # Verify balance factor for all nodes
        assert self._is_balanced(tree._root)

    def _is_balanced(self, node: Optional[Node]) -> bool:
        """Helper method to verify all nodes have balance factor in [-1, 1]."""
        if node is None:
            return True
        
        balance = self._get_balance_factor(node)
        if abs(balance) > 1:
            return False
        
        return self._is_balanced(node.left) and self._is_balanced(node.right)

    def _get_balance_factor(self, node: Node) -> int:
        """Helper method to calculate balance factor."""
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        return left_height - right_height


class TestAVLTreeDeletion:
    """Tests for deletion operations."""

    def test_delete_leaf_node(self):
        """Test deleting a leaf node."""
        tree = AVLTree()
        tree.insert({"document": 50, "name": "A"})
        tree.insert({"document": 30, "name": "B"})
        tree.insert({"document": 70, "name": "C"})
        
        result = tree.delete(30)
        assert result is True
        assert tree.size() == 2
        assert tree.search(30) is None

    def test_delete_node_with_one_child(self):
        """Test deleting a node with one child."""
        tree = AVLTree()
        tree.insert({"document": 50, "name": "A"})
        tree.insert({"document": 30, "name": "B"})
        tree.insert({"document": 20, "name": "C"})
        
        result = tree.delete(30)
        assert result is True
        assert tree.size() == 2
        assert tree.search(30) is None
        assert tree.search(20) is not None

    def test_delete_node_with_two_children(self):
        """Test deleting a node with two children."""
        tree = AVLTree()
        tree.insert({"document": 50, "name": "A"})
        tree.insert({"document": 30, "name": "B"})
        tree.insert({"document": 70, "name": "C"})
        tree.insert({"document": 20, "name": "D"})
        tree.insert({"document": 40, "name": "E"})
        
        result = tree.delete(30)
        assert result is True
        assert tree.size() == 4
        assert tree.search(30) is None
        
        # Verify tree structure is maintained
        in_order = tree.in_order()
        assert [node["document"] for node in in_order] == [20, 40, 50, 70]

    def test_delete_root_node(self):
        """Test deleting the root node."""
        tree = AVLTree()
        tree.insert({"document": 50, "name": "A"})
        tree.insert({"document": 30, "name": "B"})
        tree.insert({"document": 70, "name": "C"})
        
        result = tree.delete(50)
        assert result is True
        assert tree.size() == 2
        assert tree.search(50) is None

    def test_delete_non_existing_node(self):
        """Test deleting a non-existing node."""
        tree = AVLTree()
        tree.insert({"document": 50, "name": "A"})
        
        result = tree.delete(100)
        assert result is False
        assert tree.size() == 1

    def test_delete_from_empty_tree(self):
        """Test deleting from an empty tree."""
        tree = AVLTree()
        result = tree.delete(50)
        assert result is False

    def test_delete_with_rebalancing_left_left(self):
        """Test deletion that triggers left-left rebalancing."""
        tree = AVLTree()
        for doc in [50, 25, 75, 10, 30, 80, 5]:
            tree.insert({"document": doc, "name": f"P{doc}"})
        
        # Delete node that causes imbalance
        tree.delete(80)
        tree.delete(75)
        
        # Verify tree is still balanced
        assert self._is_balanced(tree._root)
        
        # Verify in-order is still sorted
        in_order = tree.in_order()
        in_order_docs = [node["document"] for node in in_order]
        assert in_order_docs == sorted(in_order_docs)

    def test_delete_with_rebalancing_right_right(self):
        """Test deletion that triggers right-right rebalancing."""
        tree = AVLTree()
        for doc in [50, 25, 75, 10, 60, 80, 90]:
            tree.insert({"document": doc, "name": f"P{doc}"})
        
        # Delete node that causes imbalance
        tree.delete(10)
        tree.delete(25)
        
        # Verify tree is still balanced
        assert self._is_balanced(tree._root)
        
        # Verify in-order is still sorted
        in_order = tree.in_order()
        in_order_docs = [node["document"] for node in in_order]
        assert in_order_docs == sorted(in_order_docs)

    def test_multiple_deletions_maintain_balance(self):
        """Test that multiple deletions maintain AVL properties."""
        tree = AVLTree()
        documents = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 55, 65, 85, 90]
        
        for doc in documents:
            tree.insert({"document": doc, "name": f"P{doc}"})
        
        # Delete multiple nodes
        to_delete = [10, 30, 75, 5]
        for doc in to_delete:
            tree.delete(doc)
        
        # Verify remaining nodes
        assert tree.size() == len(documents) - len(to_delete)
        
        # Verify tree is balanced
        assert self._is_balanced(tree._root)
        
        # Verify in-order is sorted
        in_order = tree.in_order()
        in_order_docs = [node["document"] for node in in_order]
        assert in_order_docs == sorted(in_order_docs)

    def _is_balanced(self, node: Optional[Node]) -> bool:
        """Helper method to verify all nodes have balance factor in [-1, 1]."""
        if node is None:
            return True
        
        balance = self._get_balance_factor(node)
        if abs(balance) > 1:
            return False
        
        return self._is_balanced(node.left) and self._is_balanced(node.right)

    def _get_balance_factor(self, node: Node) -> int:
        """Helper method to calculate balance factor."""
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        return left_height - right_height


class TestAVLTreeTraversals:
    """Tests for tree traversal operations."""

    def test_in_order_traversal(self):
        """Test in-order traversal returns documents in ascending order."""
        tree = AVLTree()
        documents = [50, 30, 70, 20, 40, 60, 80]
        
        for doc in documents:
            tree.insert({"document": doc, "name": f"Person{doc}"})
        
        in_order = tree.in_order()
        in_order_docs = [node["document"] for node in in_order]
        
        assert in_order_docs == sorted(documents)

    def test_pre_order_traversal(self):
        """Test pre-order traversal."""
        tree = AVLTree()
        # Build a specific tree structure
        tree.insert({"document": 50, "name": "A"})
        tree.insert({"document": 30, "name": "B"})
        tree.insert({"document": 70, "name": "C"})
        tree.insert({"document": 20, "name": "D"})
        tree.insert({"document": 40, "name": "E"})
        
        pre_order = tree.pre_order()
        pre_order_docs = [node["document"] for node in pre_order]
        
        # Pre-order: root, left subtree, right subtree
        assert pre_order_docs[0] == 50  # Root should be first

    def test_post_order_traversal(self):
        """Test post-order traversal."""
        tree = AVLTree()
        tree.insert({"document": 50, "name": "A"})
        tree.insert({"document": 30, "name": "B"})
        tree.insert({"document": 70, "name": "C"})
        tree.insert({"document": 20, "name": "D"})
        tree.insert({"document": 40, "name": "E"})
        
        post_order = tree.post_order()
        post_order_docs = [node["document"] for node in post_order]
        
        # Post-order: left subtree, right subtree, root
        assert post_order_docs[-1] == 50  # Root should be last

    def test_traversals_on_empty_tree(self):
        """Test traversals on an empty tree."""
        tree = AVLTree()
        
        assert tree.in_order() == []
        assert tree.pre_order() == []
        assert tree.post_order() == []

    def test_traversals_on_single_node(self):
        """Test traversals on a tree with single node."""
        tree = AVLTree()
        tree.insert({"document": 50, "name": "Alice"})
        
        assert len(tree.in_order()) == 1
        assert len(tree.pre_order()) == 1
        assert len(tree.post_order()) == 1
        
        assert tree.in_order()[0]["document"] == 50
        assert tree.pre_order()[0]["document"] == 50
        assert tree.post_order()[0]["document"] == 50


class TestAVLTreeProperties:
    """Tests for AVL Tree properties and invariants."""

    def test_avl_property_after_insertions(self):
        """Test that AVL property is maintained after multiple insertions."""
        tree = AVLTree()
        documents = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 55, 65, 85, 90]
        
        for doc in documents:
            tree.insert({"document": doc, "name": f"P{doc}"})
        
        # Verify balance factor for all nodes
        assert self._is_balanced(tree._root)

    def test_bst_property_maintained(self):
        """Test that BST property is maintained (in-order is sorted)."""
        tree = AVLTree()
        documents = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 55]
        
        for doc in documents:
            tree.insert({"document": doc, "name": f"P{doc}"})
        
        in_order = tree.in_order()
        in_order_docs = [node["document"] for node in in_order]
        
        assert in_order_docs == sorted(documents)

    def test_avl_property_after_deletions(self):
        """Test that AVL property is maintained after deletions."""
        tree = AVLTree()
        documents = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 55, 65, 85, 90]
        
        for doc in documents:
            tree.insert({"document": doc, "name": f"P{doc}"})
        
        # Delete some nodes
        tree.delete(10)
        tree.delete(30)
        tree.delete(75)
        
        # Verify balance factor for all nodes
        assert self._is_balanced(tree._root)

    def test_height_calculation(self):
        """Test that node heights are calculated correctly."""
        tree = AVLTree()
        tree.insert({"document": 50, "name": "A"})
        tree.insert({"document": 30, "name": "B"})
        tree.insert({"document": 70, "name": "C"})
        
        # Root height should be 2
        assert tree._root.height == 2
        
        # Leaf nodes should have height 1
        assert tree._root.left.height == 1
        assert tree._root.right.height == 1

    def _is_balanced(self, node: Optional[Node]) -> bool:
        """Helper method to verify all nodes have balance factor in [-1, 1]."""
        if node is None:
            return True
        
        balance = self._get_balance_factor(node)
        if abs(balance) > 1:
            return False
        
        return self._is_balanced(node.left) and self._is_balanced(node.right)

    def _get_balance_factor(self, node: Node) -> int:
        """Helper method to calculate balance factor."""
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        return left_height - right_height


class TestAVLTreeUtilityMethods:
    """Tests for utility methods."""

    def test_get_min(self):
        """Test getting minimum document node."""
        tree = AVLTree()
        documents = [50, 30, 70, 20, 40, 60, 80]
        
        for doc in documents:
            tree.insert({"document": doc, "name": f"P{doc}"})
        
        min_node = tree.get_min()
        assert min_node is not None
        assert min_node["document"] == 20

    def test_get_min_empty_tree(self):
        """Test getting minimum from empty tree."""
        tree = AVLTree()
        assert tree.get_min() is None

    def test_get_max(self):
        """Test getting maximum document node."""
        tree = AVLTree()
        documents = [50, 30, 70, 20, 40, 60, 80]
        
        for doc in documents:
            tree.insert({"document": doc, "name": f"P{doc}"})
        
        max_node = tree.get_max()
        assert max_node is not None
        assert max_node["document"] == 80

    def test_get_max_empty_tree(self):
        """Test getting maximum from empty tree."""
        tree = AVLTree()
        assert tree.get_max() is None

    def test_clear_tree(self):
        """Test clearing all nodes from tree."""
        tree = AVLTree()
        for doc in [50, 30, 70, 20, 40]:
            tree.insert({"document": doc, "name": f"P{doc}"})
        
        tree.clear()
        
        assert tree.size() == 0
        assert tree.is_empty() is True
        assert tree.get_root() is None

    def test_len_operator(self):
        """Test using len() operator on tree."""
        tree = AVLTree()
        assert len(tree) == 0
        
        for doc in [50, 30, 70]:
            tree.insert({"document": doc, "name": f"P{doc}"})
        
        assert len(tree) == 3

    def test_repr_method(self):
        """Test string representation of tree."""
        tree = AVLTree()
        tree.insert({"document": 50, "name": "A"})
        
        repr_str = repr(tree)
        assert "AVLTree" in repr_str
        assert "size=1" in repr_str
        assert "root=50" in repr_str


class TestAVLTreeEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_insert_max_valid_document(self):
        """Test inserting maximum valid document (999999)."""
        tree = AVLTree()
        tree.insert({"document": 999999, "name": "Max"})
        
        assert tree.size() == 1
        assert tree.search(999999) is not None

    def test_insert_min_valid_document(self):
        """Test inserting minimum valid document (0)."""
        tree = AVLTree()
        tree.insert({"document": 0, "name": "Min"})
        
        assert tree.size() == 1
        assert tree.search(0) is not None

    def test_large_tree_operations(self):
        """Test operations on a large tree."""
        tree = AVLTree()
        num_nodes = 100
        
        # Insert many nodes
        for i in range(num_nodes):
            tree.insert({"document": i * 100, "name": f"P{i}"})
        
        assert tree.size() == num_nodes
        
        # Verify tree is balanced
        assert self._is_balanced(tree._root)
        
        # Verify in-order is sorted
        in_order = tree.in_order()
        in_order_docs = [node["document"] for node in in_order]
        assert in_order_docs == sorted(in_order_docs)

    def test_alternating_insert_delete(self):
        """Test alternating insertions and deletions."""
        tree = AVLTree()
        
        # Insert some nodes
        for doc in [50, 30, 70, 20, 40]:
            tree.insert({"document": doc, "name": f"P{doc}"})
        
        # Delete and insert alternately
        tree.delete(30)
        tree.insert({"document": 35, "name": "P35"})
        tree.delete(70)
        tree.insert({"document": 75, "name": "P75"})
        
        # Verify tree is still balanced
        assert self._is_balanced(tree._root)
        assert tree.size() == 5

    def _is_balanced(self, node: Optional[Node]) -> bool:
        """Helper method to verify all nodes have balance factor in [-1, 1]."""
        if node is None:
            return True
        
        balance = self._get_balance_factor(node)
        if abs(balance) > 1:
            return False
        
        return self._is_balanced(node.left) and self._is_balanced(node.right)

    def _get_balance_factor(self, node: Node) -> int:
        """Helper method to calculate balance factor."""
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        return left_height - right_height
