"""
AVL Tree (Self-balancing Binary Search Tree) Implementation.

This module provides a complete AVL Tree implementation with support for
insertion, search, deletion and traversals, maintaining automatic tree
balance through rotations.
"""

from __future__ import annotations
from typing import Any, Optional, List

from api_avl.model.node import Node


class AVLTree:
    """
    AVL Tree (Self-balancing Binary Search Tree).

    Maintains the AVL invariant: |balance_factor| ≤ 1 for all nodes.
    Provides efficient insertion, search and deletion operations
    with O(log n) complexity on average.
    """

    def __init__(self) -> None:
        """Initializes an empty AVL tree."""
        self._root: Optional[Node] = None
        self._size: int = 0

    def insert(self, child: dict[str, Any]) -> None:
        """
        Inserts a new node into the AVL tree.

        Maintains tree balance by applying rotations when necessary.

        Args:
            child: Dictionary with child information. Must contain
                   the 'document' key as unique identifier.

        Raises:
            KeyError: If the dictionary does not contain the 'document' key.
            ValueError: If the document already exists in the tree.
        """
        if "document" not in child:
            raise KeyError("The child object must contain the 'document' key")

        document = child["document"]
        if isinstance(document, str):
            try:
                document = int(document)
            except ValueError:
                raise ValueError(
                    f"The document '{document}' cannot be converted to integer"
                )

        self._root = self._insert_recursive(self._root, document, child)
        self._size += 1

    def _insert_recursive(
        self, node: Optional[Node], document: int, data: dict[str, Any]
    ) -> Node:
        """
        Recursively inserts a node and balances the tree.

        Args:
            node: Current node in recursion.
            document: Key of the new node.
            data: Complete data of the new node.

        Returns:
            Root node of the balanced subtree.

        Raises:
            ValueError: If the document already exists in the tree.
        """
        # Base case: insert new node
        if node is None:
            return Node(document=document, data=data)

        # Standard BST insertion
        if document < node.document:
            node.left = self._insert_recursive(node.left, document, data)
        elif document > node.document:
            node.right = self._insert_recursive(node.right, document, data)
        else:
            raise ValueError(f"The document {document} already exists in the tree")

        # Update current node height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Get balance factor
        balance = self.get_balance(node)

        # Left-Left case: right rotation
        if balance > 1 and node.left and document < node.left.document:
            return self._rotate_right(node)

        # Right-Right case: left rotation
        if balance < -1 and node.right and document > node.right.document:
            return self._rotate_left(node)

        # Left-Right case: left-right rotation
        if balance > 1 and node.left and document > node.left.document:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right-Left case: right-left rotation
        if balance < -1 and node.right and document < node.right.document:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def search(self, document: int | str) -> Optional[dict[str, Any]]:
        """
        Searches for a node by its document and returns its complete data.

        Args:
            document: Key of the node to search.

        Returns:
            Dictionary with node data if it exists, None otherwise.
        """
        if isinstance(document, str):
            try:
                document = int(document)
            except ValueError:
                return None

        node = self._search_recursive(self._root, document)
        return node.data if node else None

    def _search_recursive(self, node: Optional[Node], document: int) -> Optional[Node]:
        """
        Recursively searches for a node by its document.

        Args:
            node: Current node in recursion.
            document: Key of the node to search.

        Returns:
            Found node or None.
        """
        if node is None or node.document == document:
            return node

        if document < node.document:
            return self._search_recursive(node.left, document)
        return self._search_recursive(node.right, document)

    def delete(self, document: int | str) -> bool:
        """
        Deletes a node from the tree by its document.

        Maintains tree balance after deletion.

        Args:
            document: Key of the node to delete.

        Returns:
            True if the node was deleted, False if it did not exist.
        """
        if isinstance(document, str):
            try:
                document = int(document)
            except ValueError:
                return False

        initial_size = self._size
        self._root = self._delete_recursive(self._root, document)
        return self._size < initial_size

    def _delete_recursive(self, node: Optional[Node], document: int) -> Optional[Node]:
        """
        Recursively deletes a node and balances the tree.

        Args:
            node: Current node in recursion.
            document: Key of the node to delete.

        Returns:
            Root node of the balanced subtree.
        """
        if node is None:
            return None

        # Standard BST search
        if document < node.document:
            node.left = self._delete_recursive(node.left, document)
        elif document > node.document:
            node.right = self._delete_recursive(node.right, document)
        else:
            # Node found - proceed with deletion
            self._size -= 1

            # Case 1: Leaf node or node with one child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Case 2: Node with two children
            # Find in-order successor (minimum of right subtree)
            successor = self._find_min(node.right)
            node.document = successor.document
            node.data = successor.data
            node.right = self._delete_recursive(node.right, successor.document)
            self._size += 1  # Compensate for decrement in recursive call

        # Update height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        # Get balance factor
        balance = self.get_balance(node)

        # Balancing after deletion
        # Left-Left case
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Left-Right case
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right-Right case
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Right-Left case
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _find_min(self, node: Node) -> Node:
        """
        Finds the node with the minimum value in a subtree.

        Args:
            node: Root of the subtree.

        Returns:
            Node with the minimum value.
        """
        current = node
        while current.left is not None:
            current = current.left
        return current

    def in_order(self) -> List[dict[str, Any]]:
        """
        In-order traversal of the tree (left-root-right).

        Returns:
            List with data from each node in ascending order by document.
        """
        result: List[dict[str, Any]] = []
        self._in_order_recursive(self._root, result)
        return result

    def _in_order_recursive(self, node: Optional[Node], result: List[dict[str, Any]]) -> None:
        """
        Recursive in-order traversal.

        Args:
            node: Current node.
            result: List where results are accumulated.
        """
        if node is not None:
            self._in_order_recursive(node.left, result)
            result.append(node.data)
            self._in_order_recursive(node.right, result)

    def pre_order(self) -> List[dict[str, Any]]:
        """
        Pre-order traversal of the tree (root-left-right).

        Returns:
            List with data from each node in pre-order.
        """
        result: List[dict[str, Any]] = []
        self._pre_order_recursive(self._root, result)
        return result

    def _pre_order_recursive(self, node: Optional[Node], result: List[dict[str, Any]]) -> None:
        """
        Recursive pre-order traversal.

        Args:
            node: Current node.
            result: List where results are accumulated.
        """
        if node is not None:
            result.append(node.data)
            self._pre_order_recursive(node.left, result)
            self._pre_order_recursive(node.right, result)

    def post_order(self) -> List[dict[str, Any]]:
        """
        Post-order traversal of the tree (left-right-root).

        Returns:
            List with data from each node in post-order.
        """
        result: List[dict[str, Any]] = []
        self._post_order_recursive(self._root, result)
        return result

    def _post_order_recursive(self, node: Optional[Node], result: List[dict[str, Any]]) -> None:
        """
        Recursive post-order traversal.

        Args:
            node: Current node.
            result: List where results are accumulated.
        """
        if node is not None:
            self._post_order_recursive(node.left, result)
            self._post_order_recursive(node.right, result)
            result.append(node.data)

    def size(self) -> int:
        """
        Returns the total number of nodes in the tree.

        Returns:
            Number of nodes.
        """
        return self._size

    def get_height(self, node: Optional[Node]) -> int:
        """
        Gets the height of a node.

        Args:
            node: Node from which to get the height.

        Returns:
            Height of the node (0 if None).
        """
        if node is None:
            return 0
        return node.height

    def get_balance(self, node: Optional[Node]) -> int:
        """
        Calculates the balance factor of a node.

        The balance factor is the difference between the height of the left
        subtree and the right subtree.

        Args:
            node: Node from which to calculate the balance.

        Returns:
            Balance factor (0 if the node is None).
        """
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def _rotate_left(self, z: Node) -> Node:
        """
        Performs a simple left rotation.

        Args:
            z: Unbalanced node (root of the subtree to rotate).

        Returns:
            New root of the rotated subtree.
        """
        y = z.right
        if y is None:
            return z

        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def _rotate_right(self, z: Node) -> Node:
        """
        Performs a simple right rotation.

        Args:
            z: Unbalanced node (root of the subtree to rotate).

        Returns:
            New root of the rotated subtree.
        """
        y = z.left
        if y is None:
            return z

        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def is_empty(self) -> bool:
        """
        Checks if the tree is empty.

        Returns:
            True if the tree has no nodes, False otherwise.
        """
        return self._root is None

    def clear(self) -> None:
        """
        Removes all nodes from the tree.
        """
        self._root = None
        self._size = 0

    def get_root(self) -> Optional[dict[str, Any]]:
        """
        Gets the data from the root node.

        Returns:
            Root node data or None if the tree is empty.
        """
        return self._root.data if self._root else None

    def get_min(self) -> Optional[dict[str, Any]]:
        """
        Gets the node with the minimum document.

        Returns:
            Data from the node with the minimum document or None if the tree is empty.
        """
        if self._root is None:
            return None
        min_node = self._find_min(self._root)
        return min_node.data

    def get_max(self) -> Optional[dict[str, Any]]:
        """
        Gets the node with the maximum document.

        Returns:
            Data from the node with the maximum document or None if the tree is empty.
        """
        if self._root is None:
            return None
        current = self._root
        while current.right is not None:
            current = current.right
        return current.data

    def __len__(self) -> int:
        """
        Allows using len() with the tree.

        Returns:
            Number of nodes in the tree.
        """
        return self._size

    def __contains__(self, document: int | str) -> bool:
        """
        Allows using the 'in' operator to check existence.

        Args:
            document: Key to search.

        Returns:
            True if the document exists in the tree, False otherwise.
        """
        return self.search(document) is not None

    def __repr__(self) -> str:
        """
        String representation of the tree.

        Returns:
            Descriptive string of the tree.
        """
        return f"AVLTree(size={self._size}, root={self._root.document if self._root else None})"
