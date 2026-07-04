from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import ApplicationStatus


class ApplicationBase(BaseModel):
    position: str
    status: ApplicationStatus
    job_url: str | None = None
    notes: str | None = None
    applied_at: datetime | None = None

class ApplicationCreate(ApplicationBase):
    company_id: int

class ApplicationUpdate(BaseModel):
    position: str | None = None
    status: ApplicationStatus | None = None
    job_url: str | None = None
    notes: str | None = None
    applied_at: datetime | None = None

class ApplicationResponse(ApplicationBase):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    id: int
    user_id: int
    company_id: int
    created_at: datetime
    updated_at: datetime

class ApplicationStatResponse(BaseModel):
    total: int
    saved: int
    applied: int
    interview: int
    offer: int
    rejected: int
    accepted: int
    