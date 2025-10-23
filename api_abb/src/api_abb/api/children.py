"""
API endpoints for managing children records.
"""
from typing import List, Literal
from fastapi import APIRouter, HTTPException, status, Query
from api_abb.schemas.child import (
    Child,
    ChildCreate,
    ChildUpdate,
    ChildResponse,
    MessageResponse,
    ErrorResponse
)
from api_abb.service.child_service import get_child_service


router = APIRouter(
    prefix="/children",
    tags=["children"],
    responses={
        404: {"model": ErrorResponse, "description": "Niño no encontrado"},
        400: {"model": ErrorResponse, "description": "Error de validación"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)


@router.post(
    "",
    response_model=ChildResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo niño",
    description="Inserta un nuevo registro de niño en el árbol binario de búsqueda. "
                "El documento debe ser único.",
    responses={
        201: {
            "description": "Niño creado exitosamente",
            "model": ChildResponse
        },
        400: {
            "description": "Ya existe un niño con ese documento o datos inválidos",
            "model": ErrorResponse
        }
    }
)
async def create_child(child: ChildCreate):
    """
    Crear un nuevo niño.
    
    - **documento**: Número de documento de identidad (único, mayor a 0)
    - **nombre**: Nombre completo del niño (requerido)
    - **edad**: Edad del niño entre 0 y 18 años (requerido)
    - **acudiente**: Nombre del acudiente o tutor legal (opcional)
    - **notas**: Notas adicionales sobre el niño (opcional)
    """
    try:
        service = get_child_service()
        created_child = service.create_child(child)
        return created_child
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


@router.get(
    "/{documento}",
    response_model=ChildResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un niño por documento",
    description="Busca y retorna la información de un niño específico usando su número de documento.",
    responses={
        200: {
            "description": "Niño encontrado",
            "model": ChildResponse
        },
        404: {
            "description": "Niño no encontrado",
            "model": ErrorResponse
        }
    }
)
async def get_child(documento: int):
    """
    Obtener un niño por su número de documento.
    
    - **documento**: Número de documento del niño a buscar
    """
    try:
        service = get_child_service()
        child = service.get_child(documento)
        
        if child is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró un niño con documento {documento}"
            )
        
        return child
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get(
    "",
    response_model=List[ChildResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los niños",
    description="Retorna la lista de todos los niños registrados. "
                "Se puede especificar el tipo de recorrido del árbol mediante el parámetro 'order'.",
    responses={
        200: {
            "description": "Lista de niños obtenida exitosamente",
            "model": List[ChildResponse]
        },
        400: {
            "description": "Parámetro 'order' inválido",
            "model": ErrorResponse
        }
    }
)
async def get_all_children(
    order: Literal["in", "pre", "post"] = Query(
        default="in",
        description="Tipo de recorrido del árbol: 'in' (inorder/ascendente), 'pre' (preorder), 'post' (postorder)"
    )
):
    """
    Listar todos los niños registrados.
    
    - **order**: Tipo de recorrido del árbol
        - `in`: Recorrido inorder (orden ascendente por documento)
        - `pre`: Recorrido preorder (raíz, izquierda, derecha)
        - `post`: Recorrido postorder (izquierda, derecha, raíz)
    """
    try:
        service = get_child_service()
        children = service.get_all_children(order=order)
        return children
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


@router.put(
    "/{documento}",
    response_model=ChildResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un niño",
    description="Actualiza la información de un niño existente. "
                "El campo 'documento' no puede ser modificado.",
    responses={
        200: {
            "description": "Niño actualizado exitosamente",
            "model": ChildResponse
        },
        404: {
            "description": "Niño no encontrado",
            "model": ErrorResponse
        },
        400: {
            "description": "Datos de actualización inválidos",
            "model": ErrorResponse
        }
    }
)
async def update_child(documento: int, child_update: ChildUpdate):
    """
    Actualizar la información de un niño existente.
    
    - **documento**: Número de documento del niño a actualizar (no se puede cambiar)
    - **nombre**: Nuevo nombre del niño (opcional)
    - **edad**: Nueva edad del niño (opcional)
    - **acudiente**: Nuevo acudiente (opcional)
    - **notas**: Nuevas notas (opcional)
    
    Solo se actualizarán los campos proporcionados en la petición.
    """
    try:
        service = get_child_service()
        updated_child = service.update_child(documento, child_update)
        
        if updated_child is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró un niño con documento {documento}"
            )
        
        return updated_child
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


@router.delete(
    "/{documento}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Eliminar un niño",
    description="Elimina un niño del sistema usando su número de documento.",
    responses={
        200: {
            "description": "Niño eliminado exitosamente",
            "model": MessageResponse
        },
        404: {
            "description": "Niño no encontrado",
            "model": ErrorResponse
        }
    }
)
async def delete_child(documento: int):
    """
    Eliminar un niño del sistema.
    
    - **documento**: Número de documento del niño a eliminar
    """
    try:
        service = get_child_service()
        deleted = service.delete_child(documento)
        
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró un niño con documento {documento}"
            )
        
        return MessageResponse(message=f"Niño con documento {documento} eliminado exitosamente")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )
