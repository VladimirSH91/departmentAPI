from pydantic import BaseModel, field_validator, Field
from datetime import datetime
from typing import Optional, List

from .employee import EmployeeRead

class DepartmentBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

    @field_validator("name")
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("name не может быть пустым")
        return v.strip()
    

class DepatmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    parent_id: Optional[int] = None


class DepatmentRead(DepartmentBase):
    id: int
    created_at: datetime
    employees: List[EmployeeRead] = []
    children: List['DepatmentRead'] = []

# те же замечания что и в модели: id: int можно заменить на id: uuid
