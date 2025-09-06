from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    sku: str = Field(..., description="Stock Keeping Unit")
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: Optional[str] = Field(None, description="Product category")
    unit: str = Field("unit", description="Unit of measurement")
    cost_price: float = Field(0.0, ge=0, description="Cost price")
    selling_price: float = Field(0.0, ge=0, description="Selling price")
    min_stock_level: int = Field(5, ge=0, description="Minimum stock level")
    max_stock_level: int = Field(100, ge=0, description="Maximum stock level")
    reorder_point: int = Field(10, ge=0, description="Reorder point")
    supplier: Optional[str] = Field(None, description="Supplier name")
    supplier_contact: Optional[str] = Field(None, description="Supplier contact")

class ProductCreate(ProductBase):
    current_stock: int = Field(0, ge=0, description="Initial stock quantity")

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    cost_price: Optional[float] = Field(None, ge=0)
    selling_price: Optional[float] = Field(None, ge=0)
    min_stock_level: Optional[int] = Field(None, ge=0)
    max_stock_level: Optional[int] = Field(None, ge=0)
    reorder_point: Optional[int] = Field(None, ge=0)
    supplier: Optional[str] = None
    supplier_contact: Optional[str] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    current_stock: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class StockUpdate(BaseModel):
    quantity: int = Field(..., description="Quantity to add (positive) or remove (negative)")
    reason: Optional[str] = Field(None, description="Reason for stock adjustment")
