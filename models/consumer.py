"""
Consumer Model - Represents electricity consumers
--------------------------------------------------
This is like a table in database with columns

For Viva - Explain:
- Each class = one table in database
- Each attribute = one column
- Relationships connect tables together
"""

from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum


class ConnectionType(enum.Enum):
    """Enum for connection types"""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"


class ConsumerStatus(enum.Enum):
    """Enum for consumer status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class Consumer(Base):
    __tablename__ = "consumers"
    
    # Primary Key - unique identifier for each consumer
    id = Column(Integer, primary_key=True, index=True)
    
    # Consumer details
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    connection_type = Column(Enum(ConnectionType), nullable=False)
    status = Column(Enum(ConsumerStatus), default=ConsumerStatus.ACTIVE)
    
    # Relationships - connects to other tables
    # back_populates creates two-way relationship
    # This allows: consumer.meters to get all meters for this consumer
    from sqlalchemy.orm import relationship
    meters = relationship("Meter", back_populates="consumer", cascade="all, delete-orphan")
    bills = relationship("Bill", back_populates="consumer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Consumer(id={self.id}, name={self.name}, type={self.connection_type.value})>"
