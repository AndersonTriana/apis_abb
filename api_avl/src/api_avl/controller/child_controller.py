"""
Child Controller Layer.

This module contains the business logic for child operations,
coordinating between the API routes and the service layer.
"""

from typing import Any
from fastapi import HTTPException, status

from api_avl.schemas.child import (
    ChildCreate,
    ChildUpdate,
    ChildResponse,
    ChildListResponse,
    MessageResponse
)
from api_avl.service.child_service import ChildService


class ChildController:
    """
    Controller for child-related operations.
    
    Handles business logic, validation, and error handling
    between the API layer and service layer.
    """
    
    def __init__(self, service: ChildService):
        """
        Initializes the controller with a service instance.
        
        Args:
            service: ChildService instance for data operations.
        """
        self.service = service
    
    def create_child(self, child: ChildCreate) -> ChildResponse:
        """
        Creates a new child record.
        
        Args:
            child: Child data to create.
        
        Returns:
            Created child data.
        
        Raises:
            HTTPException: 400 if document already exists or validation fails.
            HTTPException: 500 if an unexpected error occurs.
        """
        try:
            # Convert Pydantic model to dict
            child_dict = child.model_dump()
            
            # Attempt to create the child
            created_child = self.service.create_child(child_dict)
            
            return ChildResponse(**created_child)
        
        except ValueError as e:
            # Document already exists or validation error
            error_msg = str(e)
            if "already exists" in error_msg:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Child with document {child.document} already exists"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        except KeyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required field: {str(e)}"
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )
    
    def get_child(self, document: int) -> ChildResponse:
        """
        Retrieves a child by document number.
        
        Args:
            document: Document number to search for.
        
        Returns:
            Child data if found.
        
        Raises:
            HTTPException: 404 if child not found.
            HTTPException: 400 if document is invalid.
        """
        try:
            # Validate document range
            if document < 0 or document > 999999:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Document must be between 0 and 999999"
                )
            
            child = self.service.get_child(document)
            
            if child is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Child with document {document} not found"
                )
            
            return ChildResponse(**child)
        
        except HTTPException:
            raise
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )
    
    def get_all_children(self, order: str = "in") -> ChildListResponse:
        """
        Retrieves all children in the specified order.
        
        Args:
            order: Traversal order ('in', 'pre', or 'post').
        
        Returns:
            List of all children with metadata.
        
        Raises:
            HTTPException: 400 if order parameter is invalid.
        """
        try:
            # Validate order parameter
            valid_orders = ["in", "pre", "post"]
            order = order.lower()
            
            if order not in valid_orders:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid order '{order}'. Must be one of: {', '.join(valid_orders)}"
                )
            
            children = self.service.get_all_children(order)
            total = self.service.get_tree_size()
            
            # Convert children to response models
            children_response = [ChildResponse(**child) for child in children]
            
            return ChildListResponse(
                total=total,
                order=order,
                children=children_response
            )
        
        except HTTPException:
            raise
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )
    
    def update_child(self, document: int, child_update: ChildUpdate) -> ChildResponse:
        """
        Updates an existing child record.
        
        Args:
            document: Document number of the child to update.
            child_update: Fields to update.
        
        Returns:
            Updated child data.
        
        Raises:
            HTTPException: 404 if child not found.
            HTTPException: 400 if validation fails or no fields to update.
        """
        try:
            # Validate document range
            if document < 0 or document > 999999:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Document must be between 0 and 999999"
                )
            
            # Convert to dict, excluding None values
            update_dict = child_update.model_dump(exclude_none=True)
            
            if not update_dict:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No fields to update"
                )
            
            # Attempt to update
            updated_child = self.service.update_child(document, update_dict)
            
            if updated_child is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Child with document {document} not found"
                )
            
            return ChildResponse(**updated_child)
        
        except HTTPException:
            raise
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )
    
    def delete_child(self, document: int) -> MessageResponse:
        """
        Deletes a child record.
        
        Args:
            document: Document number of the child to delete.
        
        Returns:
            Success message.
        
        Raises:
            HTTPException: 404 if child not found.
            HTTPException: 400 if document is invalid.
        """
        try:
            # Validate document range
            if document < 0 or document > 999999:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Document must be between 0 and 999999"
                )
            
            deleted = self.service.delete_child(document)
            
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Child with document {document} not found"
                )
            
            return MessageResponse(
                message=f"Child with document {document} deleted successfully"
            )
        
        except HTTPException:
            raise
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )
    
    def get_tree_info(self) -> dict[str, Any]:
        """
        Gets information about the AVL tree state.
        
        Returns:
            Dictionary with tree statistics.
        """
        try:
            return self.service.get_tree_info()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal server error: {str(e)}"
            )
