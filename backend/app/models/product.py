from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.database.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, index=True)
    unit = Column(String, default="unit")  # unit, kg, lb, etc.
    
    # Pricing
    cost_price = Column(Float, default=0.0)
    selling_price = Column(Float, default=0.0)
    
    # Stock levels
    current_stock = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=5)
    max_stock_level = Column(Integer, default=100)
    reorder_point = Column(Integer, default=10)
    
    # Supplier info
    supplier = Column(String)
    supplier_contact = Column(String)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
