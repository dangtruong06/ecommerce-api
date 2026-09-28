# Products Router 
# Endpoints for products - simple/short and operations are in /api/db/products.py

from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.params import Depends
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

@router.get("/")
def list_products(session: Session = Depends(get_db), skip: int = Query(0, ge=0), 
                  limit: int = Query(10, ge=1, le=100)) -> list[Product]:
    db_products = list_db_products(session, skip, limit)
    return [Product(**p.__dict__) for p in db_products]