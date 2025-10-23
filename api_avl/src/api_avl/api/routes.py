"""
API Routes for Children Management.

This module defines all REST API endpoints for managing children
stored in an AVL tree.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, status

from api_avl.schemas.child import (
    ChildCreate,
    ChildUpdate,
    ChildResponse,
    ChildListResponse,
    MessageResponse,
    ErrorResponse
)
from api_avl.controller.child_controller import ChildController
from api_avl.service.child_service import get_child_service, ChildService


# Create router
router = APIRouter(
    prefix="/children",
    tags=["children"],
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Internal Server Error"
        }
    }
)


def get_child_controller(
    service: Annotated[ChildService, Depends(get_child_service)]
) -> ChildController:
    """
    Dependency injection for ChildController.
    
    Args:
        service: Injected ChildService instance.
    
    Returns:
        ChildController instance.
    """
    return ChildController(service)


@router.post(
    "/",
    response_model=ChildResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new child",
    description="Inserts a new child record into the AVL tree. The document must be unique.",
    responses={
        201: {
            "description": "Child created successfully",
            "model": ChildResponse
        },
        400: {
            "description": "Bad Request - Document already exists or validation error",
            "model": ErrorResponse
        }
    }
)
def create_child(
    child: ChildCreate,
    controller: Annotated[ChildController, Depends(get_child_controller)]
) -> ChildResponse:
    """
    Create a new child record.
    
    - **document**: Unique document number (0-999999)
    - **first_name**: Child's first name
    - **last_name**: Child's last name
    - **birth_date**: Birth date in YYYY-MM-DD format
    - **gender**: Gender (male, female, or other)
    - **address**: Residential address
    - **phone**: Contact phone number
    - **email**: Contact email (optional)
    """
    return controller.create_child(child)


@router.get(
    "/{document}",
    response_model=ChildResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a child by document",
    description="Retrieves a child record by its unique document number.",
    responses={
        200: {
            "description": "Child found",
            "model": ChildResponse
        },
        404: {
            "description": "Child not found",
            "model": ErrorResponse
        },
        400: {
            "description": "Invalid document format",
            "model": ErrorResponse
        }
    }
)
def get_child(
    document: int,
    controller: Annotated[ChildController, Depends(get_child_controller)]
) -> ChildResponse:
    """
    Get a child by document number.
    
    - **document**: The unique document number to search for (0-999999)
    """
    return controller.get_child(document)


@router.get(
    "/",
    response_model=ChildListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all children",
    description="Retrieves all children in the specified traversal order.",
    responses={
        200: {
            "description": "List of children",
            "model": ChildListResponse
        },
        400: {
            "description": "Invalid order parameter",
            "model": ErrorResponse
        }
    }
)
def get_all_children(
    controller: Annotated[ChildController, Depends(get_child_controller)],
    order: Annotated[str, Query(
        description="Traversal order: 'in' (in-order/sorted), 'pre' (pre-order), or 'post' (post-order)",
        pattern="^(in|pre|post)$"
    )] = "in"
) -> ChildListResponse:
    """
    List all children in the AVL tree.
    
    - **order**: Traversal order
        - **in**: In-order traversal (sorted by document, ascending)
        - **pre**: Pre-order traversal (root-left-right)
        - **post**: Post-order traversal (left-right-root)
    """
    return controller.get_all_children(order)


@router.put(
    "/{document}",
    response_model=ChildResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a child",
    description="Updates an existing child record. The document field cannot be changed.",
    responses={
        200: {
            "description": "Child updated successfully",
            "model": ChildResponse
        },
        404: {
            "description": "Child not found",
            "model": ErrorResponse
        },
        400: {
            "description": "Bad Request - Validation error or no fields to update",
            "model": ErrorResponse
        }
    }
)
def update_child(
    document: int,
    child_update: ChildUpdate,
    controller: Annotated[ChildController, Depends(get_child_controller)]
) -> ChildResponse:
    """
    Update an existing child record.
    
    - **document**: The document number of the child to update (cannot be changed)
    - **child_update**: Fields to update (all optional)
    
    Note: The document field itself cannot be updated. To change a document,
    delete the old record and create a new one.
    """
    return controller.update_child(document, child_update)


@router.delete(
    "/{document}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a child",
    description="Deletes a child record from the AVL tree by document number.",
    responses={
        200: {
            "description": "Child deleted successfully",
            "model": MessageResponse
        },
        404: {
            "description": "Child not found",
            "model": ErrorResponse
        },
        400: {
            "description": "Invalid document format",
            "model": ErrorResponse
        }
    }
)
def delete_child(
    document: int,
    controller: Annotated[ChildController, Depends(get_child_controller)]
) -> MessageResponse:
    """
    Delete a child by document number.
    
    - **document**: The unique document number of the child to delete (0-999999)
    """
    return controller.delete_child(document)


@router.get(
    "/tree/info",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get tree information",
    description="Returns statistics about the current state of the AVL tree.",
    tags=["tree-info"]
)
def get_tree_info(
    controller: Annotated[ChildController, Depends(get_child_controller)]
) -> dict:
    """
    Get AVL tree statistics.
    
    Returns information such as:
    - Total number of children
    - Whether the tree is empty
    - Root document
    - Minimum and maximum documents
    """
    return controller.get_tree_info()
