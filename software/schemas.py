from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    id: Optional[int] = None
    name: str
    category: str
    price: int
    description: Optional[str] = None
    quantity_in_stock: int


class ProductResponse(ProductCreate):
    class Config:
        from_attributes = True


class ProductPatch(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    quantity_in_stock: Optional[int] = None


class OrderCreate(BaseModel):
    id: Optional[int] = None
    customer_name: str
    order_date: Optional[datetime] = None
    quantity_ordered: int
    product_id: int


class OrderResponse(OrderCreate):
    class Config:
        from_attributes = True


class OrderPatch(BaseModel):
    id: Optional[int] = None
    customer_name: Optional[str] = None
    order_date: Optional[datetime] = None
    quantity_ordered: Optional[int] = None
    product_id: Optional[int] = None
