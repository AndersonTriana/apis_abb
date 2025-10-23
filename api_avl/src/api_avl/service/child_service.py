"""
Child Service Layer.

This module provides the service layer for managing children in the AVL tree.
It acts as a singleton to maintain a single tree instance in memory.
"""

from typing import Optional, List, Any
from api_avl.model.avl_tree import AVLTree


class ChildService:
    """
    Service class for managing children in an AVL tree.
    
    Implements the Singleton pattern to ensure a single tree instance
    is shared across the application.
    """
    
    _instance: Optional["ChildService"] = None
    _tree: AVLTree
    
    def __new__(cls) -> "ChildService":
        """
        Implements Singleton pattern.
        
        Returns:
            The single instance of ChildService.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tree = AVLTree()
        return cls._instance
    
    def create_child(self, child_data: dict[str, Any]) -> dict[str, Any]:
        """
        Inserts a new child into the AVL tree.
        
        Args:
            child_data: Dictionary with child information including document.
        
        Returns:
            The inserted child data.
        
        Raises:
            ValueError: If the document already exists or is invalid.
            KeyError: If required fields are missing.
        """
        self._tree.insert(child_data)
        return child_data
    
    def get_child(self, document: int) -> Optional[dict[str, Any]]:
        """
        Retrieves a child by document number.
        
        Args:
            document: The document number to search for.
        
        Returns:
            Child data if found, None otherwise.
        """
        return self._tree.search(document)
    
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
            return self._tree.in_order()
        elif order == "pre":
            return self._tree.pre_order()
        elif order == "post":
            return self._tree.post_order()
        else:
            raise ValueError(
                f"Invalid order '{order}'. Must be 'in', 'pre', or 'post'"
            )
    
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
        existing_child = self._tree.search(document)
        
        if existing_child is None:
            return None
        
        # Merge existing data with updates
        updated_child = {**existing_child, **update_data}
        
        # Ensure document remains unchanged
        updated_child["document"] = document
        
        # Delete old node and insert updated one
        self._tree.delete(document)
        self._tree.insert(updated_child)
        
        return updated_child
    
    def delete_child(self, document: int) -> bool:
        """
        Deletes a child from the AVL tree.
        
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
        return document in self._tree
    
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
        return {
            "total_children": self._tree.size(),
            "is_empty": self._tree.is_empty(),
            "root_document": self._tree.get_root()["document"] if not self._tree.is_empty() else None,
            "min_document": self._tree.get_min()["document"] if not self._tree.is_empty() else None,
            "max_document": self._tree.get_max()["document"] if not self._tree.is_empty() else None
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
