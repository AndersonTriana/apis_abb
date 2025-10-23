"""
AVL Tree Node.

This module defines the basic structure of a node for the AVL Tree.
"""

from __future__ import annotations
from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class Node:
    """
    AVL Tree Node.

    Attributes:
        document: Unique numeric key of the node (child identifier, max 6 digits).
        data: Object containing the complete child information.
        left: Reference to the left child.
        right: Reference to the right child.
        height: Height of the node in the tree (used for balancing).
    """

    document: int
    data: dict[str, Any]
    left: Optional[Node] = None
    right: Optional[Node] = None
    height: int = 1

    def __post_init__(self) -> None:
        """Validates and normalizes the document when initializing the node."""
        if isinstance(self.document, str):
            try:
                self.document = int(self.document)
            except ValueError:
                raise ValueError(
                    f"The document '{self.document}' cannot be converted to integer"
                )
        elif not isinstance(self.document, int):
            raise TypeError("The document must be an integer or convertible string to integer")
        
        # Validate document has maximum 6 digits
        if self.document < 0 or self.document > 999999:
            raise ValueError(
                f"The document must be between 0 and 999999 (max 6 digits), got {self.document}"
            )
