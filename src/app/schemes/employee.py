from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional


class EmployeBase(BaseModel):
    department_id: int
    full_name: str
    position: str
    hired_at: Optional[date] = None

    @field_validator("full_name")
    def full_name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("full_name не может быть пустым")
        if len(v) > 200:
            raise ValueError("full_name не может быть длиннее 200 символов")
        return v.strip()
    
    @field_validator("position")
    def position_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("position не может быть пустым")
        if len(v) > 200:
            raise ValueError("position не может быть длиннее 200 символов")
        return v.strip()


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