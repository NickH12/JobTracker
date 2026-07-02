from app.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

def utc_now():
    return datetime.now(tz=timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # Primary key
    email = Column(String(255), unique=True, index=True, nullable=False) # limit the string to 255 length
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    companies = relationship("Company", back_populates="user", cascade="all, delete-orphan") # Ensure that when a User is deleted, all their associated Companies are also deleted
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan") # Ensure that when a User is deleted, all their associated Applications are also deleted