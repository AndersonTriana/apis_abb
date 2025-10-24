"""
Pydantic schemas for Child model.
"""
from typing import Literal, Optional
from pydantic import BaseModel, Field


class ChildBase(BaseModel):
    """Base schema for Child with common fields."""
    nombre: str = Field(..., min_length=1, description="Nombre completo del niño")
    edad: int = Field(..., ge=0, le=18, description="Edad del niño (0-18 años)")
    ciudad: str = Field(..., min_length=1, description="Ciudad de residencia del niño")
    genero: Literal["Masculino", "Femenino"] = Field(..., description="Género del niño")
    acudiente: Optional[str] = Field(None, description="Nombre del acudiente o tutor legal")
    notas: Optional[str] = Field(None, description="Notas adicionales sobre el niño")


class ChildCreate(ChildBase):
    """Schema for creating a new child."""
    documento: int = Field(..., gt=0, description="Número de documento de identidad (único)")


class ChildUpdate(ChildBase):
    """Schema for updating an existing child (documento cannot be changed)."""
    nombre: Optional[str] = Field(None, min_length=1, description="Nombre completo del niño")
    edad: Optional[int] = Field(None, ge=0, le=18, description="Edad del niño (0-18 años)")
    ciudad: Optional[str] = Field(None, min_length=1, description="Ciudad de residencia del niño")
    genero: Optional[Literal["Masculino", "Femenino"]] = Field(None, description="Género del niño")


class Child(ChildBase):
    """Complete Child schema with all fields."""
    documento: int = Field(..., gt=0, description="Número de documento de identidad (único)")

    class Config:
        json_schema_extra = {
            "example": {
                "documento": 1234567890,
                "nombre": "Juan Pérez",
                "edad": 10,
                "ciudad": "Bogotá",
                "genero": "Masculino",
                "acudiente": "María Pérez",
                "notas": "Alérgico al maní"
            }
        }


class ChildResponse(Child):
    """Response schema for Child operations."""
    pass


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operación exitosa"
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Descripción del error"
            }
        }


class CityGenderReport(BaseModel):
    """DTO for city and gender report."""
    ciudad: str = Field(..., description="Nombre de la ciudad")
    masculino: int = Field(..., ge=0, description="Cantidad de niños de género masculino")
    femenino: int = Field(..., ge=0, description="Cantidad de niños de género femenino")
    total: int = Field(..., ge=0, description="Total de niños en la ciudad")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ciudad": "Manizales",
                "masculino": 10,
                "femenino": 8,
                "total": 18
            }
        }
