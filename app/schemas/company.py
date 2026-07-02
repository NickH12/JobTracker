from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CompanyBase(BaseModel):
    name: str
    website: str | None = None
    notes: str | None = None


class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
