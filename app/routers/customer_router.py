from typing import List

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)

from app.services.customer_service import CustomerService


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.get("/", response_model=List[CustomerResponse])
def get_customers(
    db: Session = Depends(get_db),
    service: CustomerService = Depends(CustomerService),
):

    return service.get_all(db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    service: CustomerService = Depends(CustomerService),
):

    return service.get_by_id(db, customer_id)


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    service: CustomerService = Depends(CustomerService),
):

    return service.create(db, payload)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    payload: CustomerUpdate,
    db: Session = Depends(get_db),
    service: CustomerService = Depends(CustomerService),
):

    return service.update(db, customer_id, payload)


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    service: CustomerService = Depends(CustomerService),
):

    return service.delete(db, customer_id)
