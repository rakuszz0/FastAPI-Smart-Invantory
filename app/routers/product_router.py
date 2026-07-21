from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

from app.services.product_service import ProductService
from app.dependencies.services import get_product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get(
    "/",
    response_model=List[ProductResponse]
)
def get_products(
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service),
):

    return service.get_all(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service),
):

    return service.get_by_id(
        db,
        product_id
    )


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201
)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service),
):

    return service.create(
        db,
        payload
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service),
):

    return service.update(
        db,
        product_id,
        payload
    )


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service),
):

    return service.delete(
        db,
        product_id
    )


@router.get(
    "/search/",
    response_model=List[ProductResponse]
)
def search_product(
    keyword: str = Query(...),
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service),
):

    return service.search(
        db,
        keyword
    )


@router.get(
    "/low-stock/",
    response_model=List[ProductResponse]
)
def low_stock(
    minimum: int = 10,
    db: Session = Depends(get_db),
    service: ProductService = Depends(get_product_service),
):

    return service.low_stock(
        db,
        minimum
    )