"""
Meter Model - Represents electricity meters
--------------------------------------------
Each consumer can have one or more meters
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum


class MeterStatus(enum.Enum):
    """Meter status options"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAULTY = "faulty"


class Meter(Base):
    __tablename__ = "meters"
    
    id = Column(Integer, primary_key=True, index=True)
    meter_number = Column(String, unique=True, nullable=False, index=True)
    status = Column(Enum(MeterStatus), default=MeterStatus.ACTIVE)
    
    # Foreign Key - links this meter to a consumer
    # When you see ForeignKey, think: "This column points to another table"
    consumer_id = Column(Integer, ForeignKey("consumers.id"), nullable=False)
    
    # Relationships
    consumer = relationship("Consumer", back_populates="meters")
    readings = relationship("MeterReading", back_populates="meter", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Meter(id={self.id}, number={self.meter_number})>"
