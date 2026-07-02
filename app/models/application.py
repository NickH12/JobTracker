from app.db.base import Base
from sqlalchemy import Column, Enum, ForeignKey, Integer, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.models.enums import ApplicationStatus

def utc_now():
    return datetime.now(tz=timezone.utc)


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True) # Primary key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Foreign key to users table
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False) # Foreign key to companies table
    position = Column(String(255), index=True, nullable=False)
    status = Column(Enum(ApplicationStatus, name="application_status"), index=True, nullable=False)
    job_url = Column(String(255), nullable=True)
    notes = Column(String(1000), nullable=True)
    applied_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    company = relationship("Company", back_populates="applications")
    user = relationship("User", back_populates="applications")
