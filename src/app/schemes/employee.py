from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class EmployeBase(BaseModel):
    department_id: int
    full_name: str
    position: str
    hired_at: Optional[date] = None


class EmployeeCreate(EmployeBase):
    pass


class EmployeeUpdate(BaseModel):
    department_id: Optional[int] = None
    full_name: Optional[str] = Field(None, min_length=1)
    position: Optional[str] = Field(None, min_length=1)
    hired_at: Optional[date] = None


class EmployeeRead(EmployeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True