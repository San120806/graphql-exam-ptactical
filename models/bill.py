"""
Bill Model - Represents electricity bills
------------------------------------------
Generated based on meter readings
"""

from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum


class BillStatus(enum.Enum):
    """Bill status options"""
    GENERATED = "generated"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Bill(Base):
    __tablename__ = "bills"
    
    id = Column(Integer, primary_key=True, index=True)
    billing_cycle = Column(String, nullable=False)  # e.g., "2024-01", "Jan-2024"
    total_units = Column(Float, nullable=False)  # Units consumed (calculated)
    amount = Column(Float, nullable=False)  # Amount to pay
    status = Column(Enum(BillStatus), default=BillStatus.GENERATED)
    generated_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    
    # Foreign Key - which consumer this bill belongs to
    consumer_id = Column(Integer, ForeignKey("consumers.id"), nullable=False)
    
    # Relationships
    consumer = relationship("Consumer", back_populates="bills")
    payments = relationship("Payment", back_populates="bill", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Bill(id={self.id}, consumer_id={self.consumer_id}, cycle={self.billing_cycle}, amount={self.amount})>"
