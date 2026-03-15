"""
Database Configuration
----------------------
This file sets up the connection to SQLite database.

Key Concepts for Viva:
1. SQLAlchemy: Python ORM that lets us work with database using Python objects
2. Session: A workspace for all database operations (like a transaction)
3. Base: The parent class for all our models
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Database URL - SQLite creates a file named 'electricity_billing.db' in current folder
DATABASE_URL = "sqlite:///./electricity_billing.db"

# Create engine - this manages the connection to database
# check_same_thread=False: Allows SQLite to be used with multiple threads (needed for async)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Set to True to see SQL queries in console (useful for debugging)
)

# Session factory - creates new sessions for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Scoped session - ensures thread-safe database access
db_session = scoped_session(SessionLocal)

# Base class for all models - all our table classes will inherit from this
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """
    Initialize database - creates all tables
    This is called when the app starts
    """
    # Import all models here so they are registered with Base
    from models import Consumer, Meter, MeterReading, Bill, Payment
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Get database session
    Used in GraphQL resolvers to perform database operations
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
