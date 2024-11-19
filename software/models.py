from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone, timedelta

class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), index=True, unique=True)
    category = Column(String(45))
    price = Column(Integer)
    description = Column(String(255), nullable=True)
    quantity_in_stock = Column(Integer)

    orders = relationship("Orders", back_populates="product")


class Orders(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(45))
    order_date = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(hours=2))
    quantity_ordered = Column(Integer)
    product_id = Column(Integer, ForeignKey('Product.id'))

    product = relationship("Product", back_populates="orders")
