from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


def utc_now():
    return datetime.now(tz=timezone.utc)

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True) # Primary key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Foreign key to users table
    name = Column(String(255), index=True, nullable=False)
    website = Column(String(255), nullable=True)
    notes = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    user = relationship("User", back_populates="companies")
    applications = relationship("Application", back_populates="company", cascade="all, delete-orphan") # Ensure that when a Company is deleted, all their associated Applications are also deleted