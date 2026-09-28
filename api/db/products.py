from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from .core import DBProduct, NotFoundError

class Product(BaseModel):
    id: int
    name: str 
    price: float
    description: Optional[str] = None
    stock: int

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

# CREATE PRODUCT
def create_db_product(product: ProductCreate, session: Session) -> DBProduct:
    db_product = DBProduct(**product.model_dump(exclude_none=True))
    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product

# READ PRODUCT
def read_db_product(product_id: int, session: Session) -> DBProduct:
    db_product = session.query(DBProduct).filter(DBProduct.id == product_id).first()
    if db_product is None:
        raise NotFoundError(f"Product with id {product_id} not found.")
    return db_product

# LIST PRODUCTS
def list_db_products(session: Session, skip: int = 0, limit: int = 10) -> list[DBProduct]:
    db_products = session.query(DBProduct).order_by(DBProduct.id).offset(skip).limit(limit).all()

    return db_products

# UPDATE PRODUCT
def update_db_product(product_id: int, product: ProductUpdate, session: Session) -> DBProduct:
    db_product = read_db_product(product_id, session)

    for key, value in product.model_dump(exclude_none=True).items():
        setattr(db_product, key, value)
    session.commit()
    session.refresh(db_product)

    return db_product

# DELETE PRODUCT
def delete_db_product(product_id: int, session: Session) -> DBProduct:
    db_product = read_db_product(product_id, session)
    session.delete(db_product)
    session.commit()
    return db_product