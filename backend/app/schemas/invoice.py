from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from app.models.invoice import InvoiceStatus

class InvoiceItemBase(BaseModel):
    product_id: Optional[int] = None
    description: str = Field(..., description="Item description")
    quantity: float = Field(1.0, gt=0, description="Quantity")
    unit_price: float = Field(..., ge=0, description="Unit price")

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItemResponse(InvoiceItemBase):
    id: int
    invoice_id: int
    total_price: float
    
    class Config:
        from_attributes = True

class InvoiceBase(BaseModel):
    customer_name: str = Field(..., description="Customer name")
    customer_email: Optional[EmailStr] = Field(None, description="Customer email")
    customer_phone: Optional[str] = Field(None, description="Customer phone")
    customer_address: Optional[str] = Field(None, description="Customer address")
    due_date: Optional[datetime] = Field(None, description="Due date")
    tax_rate: float = Field(0.0, ge=0, le=100, description="Tax rate percentage")
    discount_rate: float = Field(0.0, ge=0, le=100, description="Discount rate percentage")
    notes: Optional[str] = Field(None, description="Invoice notes")
    payment_terms: Optional[str] = Field(None, description="Payment terms")

class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate] = Field(..., description="Invoice items")

class InvoiceUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[InvoiceStatus] = None
    notes: Optional[str] = None
    payment_terms: Optional[str] = None

class InvoiceResponse(InvoiceBase):
    id: int
    invoice_number: str
    issue_date: datetime
    status: InvoiceStatus
    subtotal: float
    tax_amount: float
    discount_amount: float
    total_amount: float
    paid_amount: float
    items: List[InvoiceItemResponse]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class PaymentRecord(BaseModel):
    amount: float = Field(..., gt=0, description="Payment amount")
    payment_method: Optional[str] = Field(None, description="Payment method")
    payment_date: Optional[datetime] = Field(None, description="Payment date")
    notes: Optional[str] = Field(None, description="Payment notes")
