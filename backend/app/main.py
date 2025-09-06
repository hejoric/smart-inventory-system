from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database.database import engine, Base, get_db
from app.api.endpoints import products, invoices
from app.services.excel_export import excel_service
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Smart Inventory Management System API"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    products.router,
    prefix=f"/api/{settings.API_VERSION}/products",
    tags=["products"]
)

app.include_router(
    invoices.router,
    prefix=f"/api/{settings.API_VERSION}/invoices",
    tags=["invoices"]
)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to Smart Inventory Management System",
        "version": settings.VERSION,
        "api_version": settings.API_VERSION,
        "docs_url": "/docs"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Excel export endpoints
@app.get("/api/{settings.API_VERSION}/export/products")
def export_products_excel(db: Session = Depends(get_db)):
    """Export all products to Excel file"""
    filepath = excel_service.export_products(db)
    filename = os.path.basename(filepath)
    return FileResponse(
        filepath,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )

@app.get("/api/{settings.API_VERSION}/export/invoices")
def export_invoices_excel(status: str = None, db: Session = Depends(get_db)):
    """Export invoices to Excel file"""
    filepath = excel_service.export_invoices(db, status)
    filename = os.path.basename(filepath)
    return FileResponse(
        filepath,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )

@app.get("/api/{settings.API_VERSION}/export/inventory-report")
def export_inventory_report(db: Session = Depends(get_db)):
    """Export comprehensive inventory report to Excel"""
    filepath = excel_service.export_inventory_report(db)
    filename = os.path.basename(filepath)
    return FileResponse(
        filepath,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )

# Dashboard statistics endpoint
@app.get("/api/{settings.API_VERSION}/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    from app.models import Product, Invoice, InvoiceStatus
    from sqlalchemy import func
    from datetime import datetime, timedelta
    
    # Product statistics
    total_products = db.query(Product).filter(Product.is_active == True).count()
    low_stock_count = db.query(Product).filter(
        Product.current_stock <= Product.reorder_point,
        Product.is_active == True
    ).count()
    out_of_stock_count = db.query(Product).filter(
        Product.current_stock == 0,
        Product.is_active == True
    ).count()
    
    # Calculate inventory value
    products = db.query(Product).filter(Product.is_active == True).all()
    total_inventory_value = sum(p.current_stock * p.cost_price for p in products)
    
    # Invoice statistics
    total_invoices = db.query(Invoice).count()
    pending_invoices = db.query(Invoice).filter(
        Invoice.status.in_([InvoiceStatus.DRAFT, InvoiceStatus.SENT])
    ).count()
    
    # Revenue calculation (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_paid_invoices = db.query(Invoice).filter(
        Invoice.status == InvoiceStatus.PAID,
        Invoice.created_at >= thirty_days_ago
    ).all()
    monthly_revenue = sum(invoice.total_amount for invoice in recent_paid_invoices)
    
    # Outstanding payments
    unpaid_invoices = db.query(Invoice).filter(
        Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.PARTIALLY_PAID])
    ).all()
    total_outstanding = sum(
        invoice.total_amount - invoice.paid_amount for invoice in unpaid_invoices
    )
    
    return {
        "products": {
            "total": total_products,
            "low_stock": low_stock_count,
            "out_of_stock": out_of_stock_count,
            "inventory_value": total_inventory_value
        },
        "invoices": {
            "total": total_invoices,
            "pending": pending_invoices,
            "monthly_revenue": monthly_revenue,
            "outstanding_amount": total_outstanding
        },
        "alerts": {
            "low_stock_products": low_stock_count,
            "overdue_invoices": db.query(Invoice).filter(
                Invoice.due_date < datetime.now(),
                Invoice.status.in_([InvoiceStatus.SENT, InvoiceStatus.PARTIALLY_PAID])
            ).count()
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
