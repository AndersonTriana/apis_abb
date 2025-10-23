"""
Child Service Layer.

This module provides the service layer for managing children in the Binary Search Tree.
It acts as a singleton to maintain a single tree instance in memory.
"""

from typing import Optional, List, Any
from api_abb.model.binary_search_tree import BinarySearchTree
from api_abb.model.node import Node


class ChildService:
    """
    Service class for managing children in a Binary Search Tree.
    
    Implements the Singleton pattern to ensure a single tree instance
    is shared across the application.
    """
    
    _instance: Optional["ChildService"] = None
    _tree: BinarySearchTree
    
    def __new__(cls) -> "ChildService":
        """
        Implements Singleton pattern.
        
        Returns:
            The single instance of ChildService.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tree = BinarySearchTree()
        return cls._instance
    
    def create_child(self, child_data: dict[str, Any]) -> dict[str, Any]:
        """
        Inserts a new child into the Binary Search Tree.
        
        Args:
            child_data: Dictionary with child information including document.
        
        Returns:
            The inserted child data.
        
        Raises:
            ValueError: If the document already exists or is invalid.
            KeyError: If required fields are missing.
        """
        # Extract document as the node ID
        document = child_data.get("documento")
        if document is None:
            raise KeyError("Field 'documento' is required")
        
        # Create a Node with the child data
        node = Node(id=document, data=child_data)
        self._tree.insert(node)
        
        return child_data
    
    def get_child(self, document: int) -> Optional[dict[str, Any]]:
        """
        Retrieves a child by document number.
        
        Args:
            document: The document number to search for.
        
        Returns:
            Child data if found, None otherwise.
        """
        node = self._tree.search(document)
        return node.data if node else None
    
    def get_all_children(self, order: str = "in") -> List[dict[str, Any]]:
        """
        Retrieves all children in the specified traversal order.
        
        Args:
            order: Traversal order ('in', 'pre', or 'post').
                  Default is 'in' (in-order, sorted by document).
        
        Returns:
            List of all children in the specified order.
        
        Raises:
            ValueError: If the order parameter is invalid.
        """
        order = order.lower()
        
        if order == "in":
            node_dicts = self._tree.inOrder()
        elif order == "pre":
            node_dicts = self._tree.preOrder()
        elif order == "post":
            node_dicts = self._tree.postOrder()
        else:
            raise ValueError(
                f"Invalid order '{order}'. Must be 'in', 'pre', or 'post'"
            )
        
        # Extract data from node dictionaries (to_dict returns {"id": ..., "data": ...})
        return [node_dict["data"] for node_dict in node_dicts]
    
    def update_child(self, document: int, update_data: dict[str, Any]) -> Optional[dict[str, Any]]:
        """
        Updates an existing child's information.
        
        The document field cannot be updated. To change a document,
        delete the old record and create a new one.
        
        Args:
            document: The document number of the child to update.
            update_data: Dictionary with fields to update (excluding document).
        
        Returns:
            Updated child data if found, None otherwise.
        """
        # Search for the existing child
        existing_node = self._tree.search(document)
        
        if existing_node is None:
            return None
        
        # Merge existing data with updates
        updated_child = {**existing_node.data, **update_data}
        
        # Ensure document remains unchanged
        updated_child["documento"] = document
        
        # Delete old node and insert updated one
        self._tree.delete(document)
        new_node = Node(id=document, data=updated_child)
        self._tree.insert(new_node)
        
        return updated_child
    
    def delete_child(self, document: int) -> bool:
        """
        Deletes a child from the Binary Search Tree.
        
        Args:
            document: The document number of the child to delete.
        
        Returns:
            True if the child was deleted, False if not found.
        """
        return self._tree.delete(document)
    
    def get_tree_size(self) -> int:
        """
        Returns the total number of children in the tree.
        
        Returns:
            Number of children stored.
        """
        return self._tree.size()
    
    def child_exists(self, document: int) -> bool:
        """
        Checks if a child with the given document exists.
        
        Args:
            document: The document number to check.
        
        Returns:
            True if the child exists, False otherwise.
        """
        return self._tree.search(document) is not None
    
    def clear_all(self) -> None:
        """
        Removes all children from the tree.
        
        Warning: This operation cannot be undone.
        """
        self._tree.clear()
    
    def get_tree_info(self) -> dict[str, Any]:
        """
        Returns information about the current state of the tree.
        
        Returns:
            Dictionary with tree statistics.
        """
        root_node = self._tree.get_root()
        min_node = self._tree.get_min()
        max_node = self._tree.get_max()
        
        return {
            "total_children": self._tree.size(),
            "is_empty": self._tree.is_empty(),
            "root_document": root_node.data["documento"] if root_node else None,
            "min_document": min_node.data["documento"] if min_node else None,
            "max_document": max_node.data["documento"] if max_node else None
        }


# Factory function to get the service instance
def get_child_service() -> ChildService:
    """
    Factory function to obtain the ChildService singleton instance.
    
    This function is used as a FastAPI dependency.
    
    Returns:
        The singleton ChildService instance.
    """
    return ChildService()
