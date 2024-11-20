from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: int
    description: Optional[str]
    quantity_in_stock: int


class ProductCreate(BaseModel):
    id: Optional[int] = None
    name: str
    category: str
    price: int
    description: Optional[str] = None
    quantity_in_stock: int


class ProductPatch(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    quantity_in_stock: Optional[int] = None


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    order_date: datetime
    quantity_ordered: int
    product_id: int


class OrderCreate(BaseModel):
    id: Optional[int] = None
    customer_name: str
    order_date: Optional[datetime] = None
    quantity_ordered: int
    product_id: int


class OrderPatch(BaseModel):
    id: Optional[int] = None
    customer_name: Optional[str] = None
    order_date: Optional[datetime] = None
    quantity_ordered: Optional[int] = None
    product_id: Optional[int] = None
