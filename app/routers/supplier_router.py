from typing import List

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.supplier import (
    SupplierCreate,
    SupplierUpdate,
    SupplierResponse,
)

from app.services.supplier_service import SupplierService
from app.dependencies.services import get_supplier_service


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)


@router.get(
    "/",
    response_model=List[SupplierResponse]
)
def get_suppliers(
    db: Session = Depends(get_db),
    service: SupplierService = Depends(get_supplier_service),
):

    return service.get_all(db)


@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse
)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    service: SupplierService = Depends(get_supplier_service),
):

    return service.get_by_id(
        db,
        supplier_id
    )


@router.post(
    "/",
    response_model=SupplierResponse,
    status_code=201
)
def create_supplier(
    payload: SupplierCreate,
    db: Session = Depends(get_db),
    service: SupplierService = Depends(get_supplier_service),
):

    return service.create(
        db,
        payload
    )


@router.put(
    "/{supplier_id}",
    response_model=SupplierResponse
)
def update_supplier(
    supplier_id: int,
    payload: SupplierUpdate,
    db: Session = Depends(get_db),
    service: SupplierService = Depends(get_supplier_service),
):

    return service.update(
        db,
        supplier_id,
        payload
    )


@router.delete("/{supplier_id}")
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    service: SupplierService = Depends(get_supplier_service),
):

    return service.delete(
        db,
        supplier_id
    )