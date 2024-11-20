from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import Product, Orders
from schemas import ProductCreate, OrderCreate, ProductResponse, OrderResponse, ProductPatch, OrderPatch
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/product/", response_model=List[ProductResponse])
async def read_product(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/product/{product_id}", response_model=ProductResponse)
async def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(product_id == Product.id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="The product with the specified ID was not found")
    return db_product


@router.post("/product/", response_model=ProductResponse)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    id_product = db.query(Product).filter(product.id == Product.id).first()
    if id_product:
        raise HTTPException(status_code=400, detail="The product with this ID already exists")

    name_product = db.query(Product).filter(product.name == Product.name).first()
    if name_product:
        raise HTTPException(status_code=400, detail="The product with this name already exists")

    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


@router.put("/product/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductResponse, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(product_id == Product.id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="The product with the specified ID was not found")

    id_product = db.query(Product).filter(product.id == Product.id, product_id != Product.id).first()
    if id_product:
        raise HTTPException(status_code=400, detail="The product with this ID already exists")

    name_product = db.query(Product).filter(product.name == Product.name, product_id != Product.id).first()
    if name_product:
        raise HTTPException(status_code=400, detail="The product with this name already exists")

    for key, value in product.dict().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/product/{product_id}", response_model=ProductResponse)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(product_id == Product.id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="The product with the specified ID was not found")

    related_orders = db.query(Orders).filter(product_id == Orders.product_id).first()
    if related_orders:
        raise HTTPException(status_code=403, detail="Cannot delete product with associated orders")

    db.delete(db_product)
    db.commit()
    return db_product


@router.patch("/product/{product_id}", response_model=ProductResponse)
async def patch_product(product_id: int, product: ProductPatch, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(product_id == Product.id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="The product with the specified ID was not found")

    updated_fields = product.dict(exclude_unset=True)

    if 'id' in updated_fields and updated_fields['id'] != product_id:
        id_product = db.query(Product).filter(Product.id == updated_fields['id']).first()
        if id_product:
            raise HTTPException(status_code=400, detail="The product with this ID already exists")

    if 'name' in updated_fields:
        name_product = db.query(Product).filter(Product.name == updated_fields['name'],
                                                product_id != Product.id).first()
        if name_product:
            raise HTTPException(status_code=400, detail="The product with this name already exists")

    for key, value in updated_fields.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/orders/", response_model=List[OrderResponse])
async def read_orders(db: Session = Depends(get_db)):
    return db.query(Orders).all()


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def read_order_by_id(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Orders).filter(order_id == Orders.id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="The order with the specified ID was not found")
    return db_order


@router.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    id_order = db.query(Orders).filter(order.id == Orders.id).first()
    if id_order:
        raise HTTPException(status_code=400, detail="The order with this ID already exists")

    id_product = db.query(Product).filter(order.product_id == Product.id).first()
    if not id_product:
        raise HTTPException(status_code=400, detail="The product with the specified ID was not found")

    db_order = Orders(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


@router.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, order: OrderResponse, db: Session = Depends(get_db)):
    db_order = db.query(Orders).filter(order_id == Orders.id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="The order with the specified ID was not found")

    id_order = db.query(Orders).filter(order.id == Orders.id, order_id != Orders.id).first()
    if id_order:
        raise HTTPException(status_code=400, detail="The order with this ID already exists")

    id_product = db.query(Product).filter(order.product_id == Product.id).first()
    if not id_product:
        raise HTTPException(status_code=400, detail="The product with the specified ID was not found")

    for key, value in order.dict().items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)

    return db_order


@router.delete("/orders/{order_id}", response_model=OrderResponse)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Orders).filter(order_id == Orders.id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="The order with the specified ID was not found")

    db.delete(db_order)
    db.commit()

    return db_order


@router.patch("/orders/{order_id}", response_model=OrderResponse)
async def patch_order(order_id: int, order: OrderPatch, db: Session = Depends(get_db)):
    db_order = db.query(Orders).filter(order_id == Orders.id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="The order with the specified ID was not found")

    updated_fields = order.dict(exclude_unset=True)

    if 'id' in updated_fields and updated_fields['id'] != order_id:
        id_order = db.query(Orders).filter(Orders.id == updated_fields['id']).first()
        if id_order:
            raise HTTPException(status_code=400, detail="The order with this ID already exists")

    if 'product_id' in updated_fields:
        id_product = db.query(Product).filter(Orders.id == updated_fields['product_id']).first()
        if not id_product:
            raise HTTPException(status_code=400, detail="The product with the specified ID was not found")

    for key, value in updated_fields.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)

    return db_order
