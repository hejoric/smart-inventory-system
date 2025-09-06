from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database.database import get_db
from app.models import Invoice, InvoiceItem, Product, InvoiceStatus
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate, InvoiceResponse, PaymentRecord
import random
import string

router = APIRouter()

def generate_invoice_number():
    """Generate unique invoice number"""
    prefix = "INV"
    year = datetime.now().year
    random_suffix = ''.join(random.choices(string.digits, k=6))
    return f"{prefix}-{year}-{random_suffix}"

@router.post("/", response_model=InvoiceResponse)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    """Create a new invoice"""
    # Generate unique invoice number
    invoice_number = generate_invoice_number()
    while db.query(Invoice).filter(Invoice.invoice_number == invoice_number).first():
        invoice_number = generate_invoice_number()
    
    # Calculate totals
    subtotal = 0
    invoice_items = []
    
    for item in invoice.items:
        total_price = item.quantity * item.unit_price
        subtotal += total_price
        
        # Create invoice item
        invoice_item = InvoiceItem(
            product_id=item.product_id,
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=total_price
        )
        invoice_items.append(invoice_item)
        
        # Update product stock if product_id is provided
        if item.product_id:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                if product.current_stock < item.quantity:
                    raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
                product.current_stock -= item.quantity
    
    # Calculate tax and discount
    tax_amount = subtotal * (invoice.tax_rate / 100)
    discount_amount = subtotal * (invoice.discount_rate / 100)
    total_amount = subtotal + tax_amount - discount_amount
    
    # Create invoice
    invoice_data = invoice.dict(exclude={'items'})
    db_invoice = Invoice(
        **invoice_data,
        invoice_number=invoice_number,
        subtotal=subtotal,
        tax_amount=tax_amount,
        discount_amount=discount_amount,
        total_amount=total_amount,
        items=invoice_items
    )
    
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

@router.get("/", response_model=List[InvoiceResponse])
def get_invoices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[InvoiceStatus] = None,
    customer_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all invoices with optional filters"""
    query = db.query(Invoice)
    
    if status:
        query = query.filter(Invoice.status == status)
    if customer_name:
        query = query.filter(Invoice.customer_name.contains(customer_name))
    
    invoices = query.offset(skip).limit(limit).all()
    return invoices

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Get a specific invoice"""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.patch("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(
    invoice_id: int,
    invoice_update: InvoiceUpdate,
    db: Session = Depends(get_db)
):
    """Update an invoice"""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    update_data = invoice_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(invoice, field, value)
    
    db.commit()
    db.refresh(invoice)
    return invoice

@router.post("/{invoice_id}/payment", response_model=InvoiceResponse)
def record_payment(
    invoice_id: int,
    payment: PaymentRecord,
    db: Session = Depends(get_db)
):
    """Record a payment for an invoice"""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    invoice.paid_amount += payment.amount
    
    # Update status based on payment
    if invoice.paid_amount >= invoice.total_amount:
        invoice.status = InvoiceStatus.PAID
    elif invoice.paid_amount > 0:
        invoice.status = InvoiceStatus.PARTIALLY_PAID
    
    db.commit()
    db.refresh(invoice)
    return invoice

@router.get("/overdue/report")
def get_overdue_invoices(db: Session = Depends(get_db)):
    """Get report of overdue invoices"""
    overdue_invoices = db.query(Invoice).filter(
        Invoice.due_date < datetime.now(),
        Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.PARTIALLY_PAID])
    ).all()
    
    report = []
    total_overdue = 0
    
    for invoice in overdue_invoices:
        days_overdue = (datetime.now() - invoice.due_date).days
        amount_due = invoice.total_amount - invoice.paid_amount
        total_overdue += amount_due
        
        report.append({
            "invoice_number": invoice.invoice_number,
            "customer_name": invoice.customer_name,
            "due_date": invoice.due_date,
            "days_overdue": days_overdue,
            "total_amount": invoice.total_amount,
            "paid_amount": invoice.paid_amount,
            "amount_due": amount_due
        })
    
    return {
        "total_overdue_invoices": len(report),
        "total_overdue_amount": total_overdue,
        "invoices": report
    }
