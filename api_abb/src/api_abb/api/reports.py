"""
API endpoints for reports and statistics.
"""
from typing import List, Annotated
from fastapi import APIRouter, Depends, status

from api_abb.schemas.child import CityGenderReport, ErrorResponse
from api_abb.controller.child_controller import ChildController
from api_abb.service.child_service import get_child_service, ChildService


router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    responses={
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
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


@router.get(
    "/children-by-city",
    response_model=List[CityGenderReport],
    status_code=status.HTTP_200_OK,
    summary="Obtener reporte de niños por ciudad y género",
    description="Genera un informe con la cantidad de niños agrupados por ciudad, "
                "discriminados por género (Masculino, Femenino) y con un total general por ciudad. "
                "Los resultados están ordenados alfabéticamente por ciudad.",
    responses={
        200: {
            "description": "Reporte generado exitosamente",
            "model": List[CityGenderReport]
        },
        500: {
            "description": "Error interno del servidor",
            "model": ErrorResponse
        }
    }
)
async def get_children_by_city_report(
    controller: Annotated[ChildController, Depends(get_child_controller)]
):
    """
    Obtener reporte de niños agrupados por ciudad y género.
    
    Retorna una lista con estadísticas por ciudad:
    - **ciudad**: Nombre de la ciudad
    - **masculino**: Cantidad de niños de género masculino
    - **femenino**: Cantidad de niños de género femenino
    - **total**: Total de niños en la ciudad
    
    Las ciudades se ordenan alfabéticamente.
    """
    return controller.get_children_by_city_report()
