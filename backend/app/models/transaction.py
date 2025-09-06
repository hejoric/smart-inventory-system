from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.database.database import Base
import enum

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class TransactionCategory(str, enum.Enum):
    SALES = "sales"
    PURCHASE = "purchase"
    SALARY = "salary"
    RENT = "rent"
    UTILITIES = "utilities"
    MARKETING = "marketing"
    EQUIPMENT = "equipment"
    OTHER = "other"

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True, nullable=False)
    
    # Transaction details
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(Enum(TransactionCategory), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    
    # Account details (for double-entry bookkeeping)
    debit_account = Column(String)
    credit_account = Column(String)
    
    # Reference
    reference_type = Column(String)  # invoice, purchase_order, etc.
    reference_id = Column(String)
    
    # Additional info
    notes = Column(Text)
    tags = Column(String)  # Comma-separated tags
    
    # Timestamps
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
