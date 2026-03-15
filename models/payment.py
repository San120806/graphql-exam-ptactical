"""
Payment Model - Records payments against bills
-----------------------------------------------
Tracks when and how much was paid
"""

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum


class PaymentStatus(enum.Enum):
    """Payment status options"""
    SUCCESS = "success"
    PENDING = "pending"
    FAILED = "failed"


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.SUCCESS)
    
    # Foreign Key - which bill this payment is for
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)
    
    # Relationship
    bill = relationship("Bill", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment(id={self.id}, bill_id={self.bill_id}, amount={self.amount})>"
