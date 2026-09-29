# Products Router 
# Endpoints for products - simple/short and operations are in /api/db/products.py

from fastapi import APIRouter, HTTPException, Request, Query, Depends
from sqlalchemy.orm import Session
from db.core import NotFoundError, get_db
from db.products import (
    Product, 
    ProductCreate,
    ProductUpdate,
    read_db_product,
    create_db_product,
    update_db_product,
    delete_db_product,
    list_db_products
)

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

# PRODUCT POST 
@router.post("/", status_code=201)
def create_product(product_create: ProductCreate, session: Session = Depends(get_db)) -> Product:
    product = create_db_product(product_create, session) 
    return Product(**product.__dict__)

# PRODUCT GET ALL
@router.get("/")
def list_products(session: Session = Depends(get_db), skip: int = Query(0, ge=0), 
                  limit: int = Query(10, ge=1, le=100)) -> list[Product]:
    db_products = list_db_products(session, skip, limit)
    return [Product(**p.__dict__) for p in db_products]

# PRODUCT GET BY ID
@router.get("/{product_id}")
def read_product(product_id: int, session: Session = Depends(get_db)) -> Product:
    try:
        product = read_db_product(product_id, session)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    
    return Product(**product.__dict__)

# PRODUCT UPDATE BY ID
@router.put("/{product_id}")
def update_product(product_id: int, product_update: ProductUpdate, session: Session = Depends(get_db)) -> Product:
    try:
        product = update_db_product(product_id, product_update, session)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e

    return Product(**product.__dict__)

# PRODUCT DELETE BY ID
@router.delete("/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_db)) -> Product:
    try:
        product = delete_db_product(product_id, session)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    
    return Product(**product.__dict__)
