from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date, datetime
from typing import Optional, List

class EmployeBase(BaseModel):
    department_id: int
    full_name: str
    position: str
    hired_at: Optional[date] = None


class EmployeeRead(EmployeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True