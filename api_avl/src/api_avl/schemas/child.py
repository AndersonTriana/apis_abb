"""
Child Pydantic Schemas.

This module defines the Pydantic models for child data validation,
serialization, and API documentation.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class ChildBase(BaseModel):
    """
    Base schema for Child with common attributes.
    
    All field names are in English as per requirements.
    """
    
    document: int = Field(
        ...,
        ge=0,
        le=999999,
        description="Unique document number (max 6 digits)",
        examples=[101]
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Child's full name",
        examples=["Ana"]
    )
    age: int = Field(
        ...,
        ge=0,
        le=18,
        description="Child's age in years",
        examples=[6]
    )
    guardian: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Guardian's name",
        examples=["María"]
    )
    
    @field_validator("name", "guardian")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validates that names contain only letters and spaces."""
        if not all(c.isalpha() or c.isspace() for c in v):
            raise ValueError("Name must contain only letters and spaces")
        return v.strip()
    
    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        """Validates that age is reasonable for a child."""
        if v < 0 or v > 18:
            raise ValueError("Age must be between 0 and 18 years")
        return v


class ChildCreate(ChildBase):
    """
    Schema for creating a new child.
    
    Inherits all fields from ChildBase.
    Used in POST /children endpoint.
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "document": 101,
                "name": "Ana",
                "age": 6,
                "guardian": "María"
            }
        }
    )


class ChildUpdate(BaseModel):
    """
    Schema for updating an existing child.
    
    All fields are optional except document is NOT allowed to be updated.
    Used in PUT /children/{document} endpoint.
    """
    
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Child's full name"
    )
    age: Optional[int] = Field(
        None,
        ge=0,
        le=18,
        description="Child's age in years"
    )
    guardian: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Guardian's name"
    )
    
    @field_validator("name", "guardian")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validates that names contain only letters and spaces."""
        if v is not None:
            if not all(c.isalpha() or c.isspace() for c in v):
                raise ValueError("Name must contain only letters and spaces")
            return v.strip()
        return v
    
    @field_validator("age")
    @classmethod
    def validate_age(cls, v: Optional[int]) -> Optional[int]:
        """Validates that age is reasonable for a child."""
        if v is not None and (v < 0 or v > 18):
            raise ValueError("Age must be between 0 and 18 years")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Ana María",
                "age": 7,
                "guardian": "María García"
            }
        }
    )


class ChildResponse(ChildBase):
    """
    Schema for child response.
    
    Used in GET responses to return complete child information.
    """
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "document": 101,
                "name": "Ana",
                "age": 6,
                "guardian": "María"
            }
        }
    )


class ChildListResponse(BaseModel):
    """
    Schema for list of children response.
    
    Used in GET /children endpoint.
    """
    
    total: int = Field(
        ...,
        description="Total number of children in the tree",
        examples=[10]
    )
    order: str = Field(
        ...,
        description="Traversal order used (in, pre, or post)",
        examples=["in"]
    )
    children: list[ChildResponse] = Field(
        ...,
        description="List of children in the specified order"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 3,
                "order": "in",
                "children": [
                    {
                        "document": 50,
                        "name": "Carlos",
                        "age": 5,
                        "guardian": "Pedro"
                    },
                    {
                        "document": 101,
                        "name": "Ana",
                        "age": 6,
                        "guardian": "María"
                    },
                    {
                        "document": 150,
                        "name": "Luis",
                        "age": 7,
                        "guardian": "Juan"
                    }
                ]
            }
        }
    )


class MessageResponse(BaseModel):
    """
    Schema for simple message responses.
    
    Used for success/error messages.
    """
    
    message: str = Field(
        ...,
        description="Response message",
        examples=["Child deleted successfully"]
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Operation completed successfully"
            }
        }
    )


class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    
    Used for error handling and validation errors.
    """
    
    detail: str = Field(
        ...,
        description="Error detail message",
        examples=["Child with document 123456 not found"]
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Validation error: invalid document format"
            }
        }
    )
