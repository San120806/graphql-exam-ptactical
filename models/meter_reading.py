"""
MeterReading Model - Records meter readings over time
------------------------------------------------------
Stores the reading value and when it was recorded
"""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class MeterReading(Base):
    __tablename__ = "meter_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    reading_value = Column(Float, nullable=False)  # The meter reading in units (kWh)
    reading_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign Key - which meter this reading belongs to
    meter_id = Column(Integer, ForeignKey("meters.id"), nullable=False)
    
    # Relationship
    meter = relationship("Meter", back_populates="readings")
    
    def __repr__(self):
        return f"<MeterReading(id={self.id}, meter_id={self.meter_id}, value={self.reading_value})>"
