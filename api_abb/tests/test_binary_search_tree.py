"""
Unit tests for the BinarySearchTree class.
"""
import pytest
from api_abb.model.node import Node
from api_abb.model.binary_search_tree import BinarySearchTree


class TestBinarySearchTreeBasics:
    """Test suite for basic BST operations."""
    
    def test_empty_tree_creation(self):
        """Test creating an empty tree."""
        bst = BinarySearchTree()
        
        assert bst.root is None
        assert bst.size() == 0
        assert bst.is_empty() is True
    
    def test_single_node_insertion(self):
        """Test inserting a single node."""
        bst = BinarySearchTree()
        node = Node(id=10, data="root")
        
        bst.insert(node)
        
        assert bst.root is not None
        assert bst.root.id == 10
        assert bst.root.data == "root"
        assert bst.size() == 1
        assert bst.is_empty() is False


class TestBinarySearchTreeInsertion:
    """Test suite for insertion operations."""
    
    def test_multiple_insertions_and_size(self):
        """Test inserting multiple nodes and validating size."""
        bst = BinarySearchTree()
        
        # Insert nodes
        bst.insert(Node(id=50, data="fifty"))
        assert bst.size() == 1
        
        bst.insert(Node(id=30, data="thirty"))
        assert bst.size() == 2
        
        bst.insert(Node(id=70, data="seventy"))
        assert bst.size() == 3
        
        bst.insert(Node(id=20, data="twenty"))
        bst.insert(Node(id=40, data="forty"))
        bst.insert(Node(id=60, data="sixty"))
        bst.insert(Node(id=80, data="eighty"))
        
        assert bst.size() == 7
    
    def test_insertion_maintains_bst_property(self):
        """Test that insertions maintain BST ordering property."""
        bst = BinarySearchTree()
        
        bst.insert(Node(id=50, data="root"))
        bst.insert(Node(id=30, data="left"))
        bst.insert(Node(id=70, data="right"))
        bst.insert(Node(id=20, data="left-left"))
        bst.insert(Node(id=40, data="left-right"))
        
        # Verify BST structure
        assert bst.root.id == 50
        assert bst.root.left.id == 30
        assert bst.root.right.id == 70
        assert bst.root.left.left.id == 20
        assert bst.root.left.right.id == 40
    
    def test_insertion_duplicate_id_raises_error(self):
        """Test that inserting duplicate id raises ValueError."""
        bst = BinarySearchTree()
        
        bst.insert(Node(id=10, data="first"))
        
        with pytest.raises(ValueError, match="already exists"):
            bst.insert(Node(id=10, data="duplicate"))
    
    def test_insertion_order_variations(self):
        """Test different insertion orders produce valid BST."""
        # Ascending order
        bst1 = BinarySearchTree()
        for i in [1, 2, 3, 4, 5]:
            bst1.insert(Node(id=i, data=f"node{i}"))
        assert bst1.size() == 5
        
        # Descending order
        bst2 = BinarySearchTree()
        for i in [5, 4, 3, 2, 1]:
            bst2.insert(Node(id=i, data=f"node{i}"))
        assert bst2.size() == 5
        
        # Random order
        bst3 = BinarySearchTree()
        for i in [3, 1, 4, 2, 5]:
            bst3.insert(Node(id=i, data=f"node{i}"))
        assert bst3.size() == 5


class TestBinarySearchTreeSearch:
    """Test suite for search operations."""
    
    def test_search_existing_nodes(self):
        """Test searching for existing nodes."""
        bst = BinarySearchTree()
        
        # Build tree
        nodes = [
            Node(id=50, data="fifty"),
            Node(id=30, data="thirty"),
            Node(id=70, data="seventy"),
            Node(id=20, data="twenty"),
            Node(id=40, data="forty"),
        ]
        for node in nodes:
            bst.insert(node)
        
        # Search for each node
        result = bst.search(50)
        assert result is not None
        assert result.id == 50
        assert result.data == "fifty"
        
        result = bst.search(30)
        assert result is not None
        assert result.id == 30
        assert result.data == "thirty"
        
        result = bst.search(20)
        assert result is not None
        assert result.id == 20
        assert result.data == "twenty"
    
    def test_search_non_existing_nodes(self):
        """Test searching for non-existing nodes."""
        bst = BinarySearchTree()
        
        bst.insert(Node(id=50, data="fifty"))
        bst.insert(Node(id=30, data="thirty"))
        bst.insert(Node(id=70, data="seventy"))
        
        # Search for non-existing ids
        assert bst.search(100) is None
        assert bst.search(10) is None
        assert bst.search(45) is None
    
    def test_search_in_empty_tree(self):
        """Test searching in an empty tree."""
        bst = BinarySearchTree()
        
        assert bst.search(10) is None
    
    def test_search_returns_complete_node_object(self):
        """Test that search returns the complete node object."""
        bst = BinarySearchTree()
        
        original_node = Node(id=25, data={"name": "test", "value": 100})
        bst.insert(original_node)
        
        found_node = bst.search(25)
        
        assert found_node is not None
        assert found_node.id == 25
        assert found_node.data == {"name": "test", "value": 100}
        assert isinstance(found_node, Node)


class TestBinarySearchTreeDeletion:
    """Test suite for deletion operations."""
    
    def test_delete_leaf_node(self):
        """Test deleting a leaf node (no children)."""
        bst = BinarySearchTree()
        
        # Build tree
        bst.insert(Node(id=50, data="fifty"))
        bst.insert(Node(id=30, data="thirty"))
        bst.insert(Node(id=70, data="seventy"))
        bst.insert(Node(id=20, data="twenty"))  # Leaf node
        
        assert bst.size() == 4
        
        # Delete leaf node
        result = bst.delete(20)
        
        assert result is True
        assert bst.size() == 3
        assert bst.search(20) is None
        assert bst.search(30) is not None  # Parent still exists
    
    def test_delete_node_with_one_child_left(self):
        """Test deleting a node with only left child."""
        bst = BinarySearchTree()
        
        # Build tree where 30 has only left child
        bst.insert(Node(id=50, data="fifty"))
        bst.insert(Node(id=30, data="thirty"))
        bst.insert(Node(id=20, data="twenty"))
        
        assert bst.size() == 3
        
        # Delete node with one left child
        result = bst.delete(30)
        
        assert result is True
        assert bst.size() == 2
        assert bst.search(30) is None
        assert bst.search(20) is not None
        assert bst.root.left.id == 20  # 20 should replace 30
    
    def test_delete_node_with_one_child_right(self):
        """Test deleting a node with only right child."""
        bst = BinarySearchTree()
        
        # Build tree where 30 has only right child
        bst.insert(Node(id=50, data="fifty"))
        bst.insert(Node(id=30, data="thirty"))
        bst.insert(Node(id=40, data="forty"))
        
        assert bst.size() == 3
        
        # Delete node with one right child
        result = bst.delete(30)
        
        assert result is True
        assert bst.size() == 2
        assert bst.search(30) is None
        assert bst.search(40) is not None
        assert bst.root.left.id == 40  # 40 should replace 30
    
    def test_delete_node_with_two_children(self):
        """Test deleting a node with two children."""
        bst = BinarySearchTree()
        
        # Build tree
        bst.insert(Node(id=50, data="fifty"))
        bst.insert(Node(id=30, data="thirty"))
        bst.insert(Node(id=70, data="seventy"))
        bst.insert(Node(id=20, data="twenty"))
        bst.insert(Node(id=40, data="forty"))
        bst.insert(Node(id=35, data="thirty-five"))
        bst.insert(Node(id=45, data="forty-five"))
        
        assert bst.size() == 7
        
        # Delete node with two children (30)
        result = bst.delete(30)
        
        assert result is True
        assert bst.size() == 6
        assert bst.search(30) is None
        
        # Verify tree structure is maintained
        # The inorder successor (35) should replace 30
        assert bst.root.left.id == 35
        assert bst.search(20) is not None
        assert bst.search(40) is not None
    
    def test_delete_root_node(self):
        """Test deleting the root node."""
        bst = BinarySearchTree()
        
        bst.insert(Node(id=50, data="fifty"))
        bst.insert(Node(id=30, data="thirty"))
        bst.insert(Node(id=70, data="seventy"))
        
        # Delete root
        result = bst.delete(50)
        
        assert result is True
        assert bst.size() == 2
        assert bst.search(50) is None
        assert bst.root.id == 70  # Inorder successor becomes root
    
    def test_delete_non_existing_node(self):
        """Test deleting a non-existing node."""
        bst = BinarySearchTree()
        
        bst.insert(Node(id=50, data="fifty"))
        bst.insert(Node(id=30, data="thirty"))
        
        initial_size = bst.size()
        result = bst.delete(100)
        
        assert result is False
        assert bst.size() == initial_size
    
    def test_delete_from_empty_tree(self):
        """Test deleting from an empty tree."""
        bst = BinarySearchTree()
        
        result = bst.delete(10)
        
        assert result is False
        assert bst.size() == 0
    
    def test_multiple_deletions(self):
        """Test multiple consecutive deletions."""
        bst = BinarySearchTree()
        
        # Insert nodes
        for i in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(Node(id=i, data=f"node{i}"))
        
        assert bst.size() == 7
        
        # Delete multiple nodes
        assert bst.delete(20) is True
        assert bst.size() == 6
        
        assert bst.delete(30) is True
        assert bst.size() == 5
        
        assert bst.delete(50) is True
        assert bst.size() == 4
        
        # Verify remaining nodes
        assert bst.search(40) is not None
        assert bst.search(60) is not None
        assert bst.search(70) is not None
        assert bst.search(80) is not None


class TestBinarySearchTreeTraversals:
    """Test suite for tree traversal operations."""
    
    def test_inorder_traversal(self):
        """Test in-order traversal returns sorted order."""
        bst = BinarySearchTree()
        
        # Insert in random order
        for id in [50, 30, 70, 20, 40, 60, 80]:
            bst.insert(Node(id=id, data=f"node{id}"))
        
        result = bst.inOrder()
        
        # In-order should return sorted ids
        ids = [node["id"] for node in result]
        assert ids == [20, 30, 40, 50, 60, 70, 80]
        
        # Verify data is included
        assert result[0]["data"] == "node20"
        assert result[3]["data"] == "node50"
    
    def test_preorder_traversal(self):
        """Test pre-order traversal."""
        bst = BinarySearchTree()
        
        # Build specific tree structure
        bst.insert(Node(id=50, data="fifty"))
        bst.insert(Node(id=30, data="thirty"))
        bst.insert(Node(id=70, data="seventy"))
        bst.insert(Node(id=20, data="twenty"))
        bst.insert(Node(id=40, data="forty"))
        
        result = bst.preOrder()
        
        # Pre-order: root, left, right
        ids = [node["id"] for node in result]
        assert ids == [50, 30, 20, 40, 70]
    
    def test_postorder_traversal(self):
        """Test post-order traversal."""
        bst = BinarySearchTree()
        
        # Build specific tree structure
        bst.insert(Node(id=50, data="fifty"))
        bst.insert(Node(id=30, data="thirty"))
        bst.insert(Node(id=70, data="seventy"))
        bst.insert(Node(id=20, data="twenty"))
        bst.insert(Node(id=40, data="forty"))
        
        result = bst.postOrder()
        
        # Post-order: left, right, root
        ids = [node["id"] for node in result]
        assert ids == [20, 40, 30, 70, 50]
    
    def test_traversals_on_empty_tree(self):
        """Test traversals on empty tree."""
        bst = BinarySearchTree()
        
        assert bst.inOrder() == []
        assert bst.preOrder() == []
        assert bst.postOrder() == []
    
    def test_traversals_on_single_node(self):
        """Test traversals on single node tree."""
        bst = BinarySearchTree()
        bst.insert(Node(id=42, data="answer"))
        
        assert len(bst.inOrder()) == 1
        assert len(bst.preOrder()) == 1
        assert len(bst.postOrder()) == 1
        
        assert bst.inOrder()[0]["id"] == 42
        assert bst.preOrder()[0]["id"] == 42
        assert bst.postOrder()[0]["id"] == 42
    
    def test_traversal_returns_dict_format(self):
        """Test that traversals return dictionaries with id and data."""
        bst = BinarySearchTree()
        
        bst.insert(Node(id=10, data="ten"))
        bst.insert(Node(id=5, data="five"))
        
        inorder_result = bst.inOrder()
        
        assert isinstance(inorder_result, list)
        assert isinstance(inorder_result[0], dict)
        assert "id" in inorder_result[0]
        assert "data" in inorder_result[0]


class TestBinarySearchTreeIntegration:
    """Integration tests for complex scenarios."""
    
    def test_bst_maintains_order_after_insertions_and_deletions(self):
        """Test that BST maintains ordering after multiple operations."""
        bst = BinarySearchTree()
        
        # Insert initial nodes
        for id in [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 65]:
            bst.insert(Node(id=id, data=f"node{id}"))
        
        # Verify initial order
        initial_inorder = bst.inOrder()
        initial_ids = [node["id"] for node in initial_inorder]
        assert initial_ids == sorted(initial_ids)
        
        # Delete some nodes
        bst.delete(30)  # Node with two children
        bst.delete(20)  # Node with two children
        bst.delete(80)  # Leaf node
        
        # Verify order is still maintained
        after_delete_inorder = bst.inOrder()
        after_delete_ids = [node["id"] for node in after_delete_inorder]
        assert after_delete_ids == sorted(after_delete_ids)
        
        # Insert more nodes
        bst.insert(Node(id=15, data="fifteen"))
        bst.insert(Node(id=75, data="seventy-five"))
        
        # Verify order is still maintained
        final_inorder = bst.inOrder()
        final_ids = [node["id"] for node in final_inorder]
        assert final_ids == sorted(final_ids)
    
    def test_complex_scenario_with_all_operations(self):
        """Test complex scenario using all BST operations."""
        bst = BinarySearchTree()
        
        # Start with empty tree
        assert bst.is_empty() is True
        assert bst.size() == 0
        
        # Insert nodes
        nodes_to_insert = [
            (50, "Product A"),
            (30, "Product B"),
            (70, "Product C"),
            (20, "Product D"),
            (40, "Product E"),
            (60, "Product F"),
            (80, "Product G"),
        ]
        
        for id, data in nodes_to_insert:
            bst.insert(Node(id=id, data=data))
        
        assert bst.size() == 7
        assert bst.is_empty() is False
        
        # Search for existing and non-existing
        found = bst.search(40)
        assert found is not None
        assert found.data == "Product E"
        
        not_found = bst.search(100)
        assert not_found is None
        
        # Verify traversals
        inorder = bst.inOrder()
        assert len(inorder) == 7
        assert [n["id"] for n in inorder] == [20, 30, 40, 50, 60, 70, 80]
        
        preorder = bst.preOrder()
        assert preorder[0]["id"] == 50  # Root first
        
        postorder = bst.postOrder()
        assert postorder[-1]["id"] == 50  # Root last
        
        # Delete nodes (all three cases)
        bst.delete(20)  # Leaf
        assert bst.size() == 6
        
        bst.delete(80)  # Leaf
        assert bst.size() == 5
        
        bst.delete(30)  # One child
        assert bst.size() == 4
        
        bst.delete(50)  # Two children (root)
        assert bst.size() == 3
        
        # Verify final state
        final_inorder = bst.inOrder()
        final_ids = [n["id"] for n in final_inorder]
        assert final_ids == sorted(final_ids)
        assert 20 not in final_ids
        assert 30 not in final_ids
        assert 50 not in final_ids
        assert 80 not in final_ids
    
    def test_clear_tree(self):
        """Test clearing the entire tree."""
        bst = BinarySearchTree()
        
        # Insert nodes
        for i in range(1, 11):
            bst.insert(Node(id=i, data=f"node{i}"))
        
        assert bst.size() == 10
        
        # Clear tree
        bst.clear()
        
        assert bst.size() == 0
        assert bst.is_empty() is True
        assert bst.root is None
        assert bst.inOrder() == []
    
    def test_rebuild_after_clear(self):
        """Test that tree can be rebuilt after clearing."""
        bst = BinarySearchTree()
        
        # First build
        for i in [5, 3, 7]:
            bst.insert(Node(id=i, data=f"first{i}"))
        
        assert bst.size() == 3
        
        # Clear
        bst.clear()
        
        # Rebuild
        for i in [10, 8, 12]:
            bst.insert(Node(id=i, data=f"second{i}"))
        
        assert bst.size() == 3
        result = bst.search(10)
        assert result is not None
        assert result.data == "second10"
        
        # Old nodes should not exist
        assert bst.search(5) is None


class TestBinarySearchTreeEdgeCases:
    """Test suite for edge cases and boundary conditions."""
    
    def test_large_tree_performance(self):
        """Test with a larger number of nodes."""
        bst = BinarySearchTree()
        
        # Insert 100 nodes
        for i in range(1, 101):
            bst.insert(Node(id=i, data=f"node{i}"))
        
        assert bst.size() == 100
        
        # Verify search works
        assert bst.search(50) is not None
        assert bst.search(1) is not None
        assert bst.search(100) is not None
        
        # Verify inorder is sorted
        inorder = bst.inOrder()
        ids = [n["id"] for n in inorder]
        assert ids == list(range(1, 101))
    
    def test_negative_ids(self):
        """Test tree with negative ids."""
        bst = BinarySearchTree()
        
        for id in [0, -10, 10, -5, 5]:
            bst.insert(Node(id=id, data=f"node{id}"))
        
        assert bst.size() == 5
        
        inorder = bst.inOrder()
        ids = [n["id"] for n in inorder]
        assert ids == [-10, -5, 0, 5, 10]
    
    def test_tree_with_complex_data_objects(self):
        """Test tree with complex data objects."""
        bst = BinarySearchTree()
        
        complex_data = [
            (1, {"name": "Alice", "age": 30, "items": [1, 2, 3]}),
            (2, {"name": "Bob", "age": 25, "items": [4, 5]}),
            (3, {"name": "Charlie", "age": 35, "items": []}),
        ]
        
        for id, data in complex_data:
            bst.insert(Node(id=id, data=data))
        
        result = bst.search(2)
        assert result.data["name"] == "Bob"
        assert result.data["age"] == 25
        assert result.data["items"] == [4, 5]
