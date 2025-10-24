"""
Child Controller Layer.

This module contains the business logic for child operations,
coordinating between the API routes and the service layer.
"""

from typing import Any
from fastapi import HTTPException, status

from api_abb.schemas.child import (
    ChildCreate,
    ChildUpdate,
    ChildResponse,
    MessageResponse,
    CityGenderReport
)
from api_abb.service.child_service import ChildService


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
                    detail=f"Ya existe un niño con documento {child.documento}"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
        
        except KeyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Campo requerido faltante: {str(e)}"
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {str(e)}"
            )
    
    def get_child(self, documento: int) -> ChildResponse:
        """
        Retrieves a child by document number.
        
        Args:
            documento: Document number to search for.
        
        Returns:
            Child data.
        
        Raises:
            HTTPException: 404 if child not found.
            HTTPException: 500 if an unexpected error occurs.
        """
        try:
            child = self.service.get_child(documento)
            
            if child is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró un niño con documento {documento}"
                )
            
            return ChildResponse(**child)
        
        except HTTPException:
            raise
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {str(e)}"
            )
    
    def get_all_children(self, order: str = "in") -> list[ChildResponse]:
        """
        Retrieves all children in the specified order.
        
        Args:
            order: Traversal order ('in', 'pre', or 'post').
        
        Returns:
            List of all children.
        
        Raises:
            HTTPException: 400 if order parameter is invalid.
            HTTPException: 500 if an unexpected error occurs.
        """
        try:
            children = self.service.get_all_children(order=order)
            return [ChildResponse(**child) for child in children]
        
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {str(e)}"
            )
    
    def update_child(self, documento: int, child_update: ChildUpdate) -> ChildResponse:
        """
        Updates an existing child's information.
        
        Args:
            documento: Document number of the child to update.
            child_update: Fields to update.
        
        Returns:
            Updated child data.
        
        Raises:
            HTTPException: 404 if child not found.
            HTTPException: 400 if validation fails.
            HTTPException: 500 if an unexpected error occurs.
        """
        try:
            # Convert Pydantic model to dict, excluding unset fields
            update_dict = child_update.model_dump(exclude_unset=True)
            
            # Attempt to update the child
            updated_child = self.service.update_child(documento, update_dict)
            
            if updated_child is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró un niño con documento {documento}"
                )
            
            return ChildResponse(**updated_child)
        
        except HTTPException:
            raise
        
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {str(e)}"
            )
    
    def delete_child(self, documento: int) -> MessageResponse:
        """
        Deletes a child from the system.
        
        Args:
            documento: Document number of the child to delete.
        
        Returns:
            Success message.
        
        Raises:
            HTTPException: 404 if child not found.
            HTTPException: 500 if an unexpected error occurs.
        """
        try:
            deleted = self.service.delete_child(documento)
            
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No se encontró un niño con documento {documento}"
                )
            
            return MessageResponse(
                message=f"Niño con documento {documento} eliminado exitosamente"
            )
        
        except HTTPException:
            raise
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {str(e)}"
            )
    
    def get_tree_info(self) -> dict[str, Any]:
        """
        Returns information about the current state of the tree.
        
        Returns:
            Dictionary with tree statistics.
        
        Raises:
            HTTPException: 500 if an unexpected error occurs.
        """
        try:
            return self.service.get_tree_info()
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {str(e)}"
            )
    
    def get_children_by_city_report(self) -> list[CityGenderReport]:
        """
        Generates a report of children grouped by city and gender.
        
        Returns:
            List of CityGenderReport objects with statistics per city.
        
        Raises:
            HTTPException: 500 if an unexpected error occurs.
        """
        try:
            report_data = self.service.get_children_by_city_report()
            return [CityGenderReport(**item) for item in report_data]
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno del servidor: {str(e)}"
            )
