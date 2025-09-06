from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.models import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, StockUpdate

router = APIRouter()

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    # Check if SKU already exists
    existing_product = db.query(Product).filter(Product.sku == product.sku).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product with this SKU already exists")
    
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductResponse])
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    low_stock: bool = False,
    db: Session = Depends(get_db)
):
    """Get all products with optional filters"""
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    if is_active is not None:
        query = query.filter(Product.is_active == is_active)
    if low_stock:
        query = query.filter(Product.current_stock <= Product.reorder_point)
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Update a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product

@router.post("/{product_id}/stock", response_model=ProductResponse)
def update_stock(
    product_id: int,
    stock_update: StockUpdate,
    db: Session = Depends(get_db)
):
    """Update product stock level"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    new_stock = product.current_stock + stock_update.quantity
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    product.current_stock = new_stock
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product (soft delete by setting is_active=False)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.is_active = False
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/low-stock/report")
def get_low_stock_report(db: Session = Depends(get_db)):
    """Get report of products with low stock"""
    products = db.query(Product).filter(
        Product.current_stock <= Product.reorder_point,
        Product.is_active == True
    ).all()
    
    report = []
    for product in products:
        report.append({
            "id": product.id,
            "sku": product.sku,
            "name": product.name,
            "current_stock": product.current_stock,
            "reorder_point": product.reorder_point,
            "suggested_order_quantity": product.max_stock_level - product.current_stock,
            "supplier": product.supplier
        })
    
    return {
        "total_products": len(report),
        "products": report
    }
