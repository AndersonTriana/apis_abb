"""
FastAPI Application for Children Management with AVL Tree.

This application provides a REST API to manage children records
stored in a self-balancing AVL tree in memory.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from api_avl.api.routes import router as children_router
from api_avl.core.exceptions import (
    validation_exception_handler,
    pydantic_validation_exception_handler,
    generic_exception_handler
)

# Create FastAPI application
app = FastAPI(
    title="Children Management API with AVL Tree",
    description="""
    REST API for managing children records stored in a self-balancing AVL tree.
    
    ## Features
    
    * **Create** a new child record
    * **Read** child records by document or list all
    * **Update** existing child records
    * **Delete** child records
    * **Tree traversals**: In-order, Pre-order, Post-order
    
    ## AVL Tree
    
    All data is stored in an AVL tree (self-balancing binary search tree) in memory.
    The tree automatically maintains balance after each insertion and deletion,
    ensuring O(log n) time complexity for all operations.
    
    ## Document Field
    
    The `document` field is the unique identifier for each child and serves as the
    key for the AVL tree. It must be a number between 0 and 999999 (max 6 digits).
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include routers
app.include_router(children_router)


@app.get(
    "/",
    tags=["root"],
    summary="Root endpoint",
    description="Returns API information and available endpoints"
)
def root():
    """
    Root endpoint providing API information.
    
    Returns basic information about the API and links to documentation.
    """
    return {
        "message": "Children Management API with AVL Tree",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "create_child": "POST /children",
            "get_child": "GET /children/{document}",
            "list_children": "GET /children?order=in|pre|post",
            "update_child": "PUT /children/{document}",
            "delete_child": "DELETE /children/{document}",
            "tree_info": "GET /children/tree/info"
        }
    }


@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    description="Returns the health status of the API"
)
def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the API.
    """
    return {
        "status": "healthy",
        "service": "Children Management API",
        "version": "1.0.0"
    }
