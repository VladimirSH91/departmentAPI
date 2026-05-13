from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from schemes import DepatmentCreate, DepatmentRead
from repositories.department import DepartmentRepository
from db.database import get_async_session

department_router = APIRouter()

@department_router.post('/department/', status_code=200)
async def add_depatment(data: DepatmentCreate, 
                        db_session: AsyncSession = Depends(get_async_session)):
    department_repo = DepartmentRepository(db_session=db_session)
    department_dict = data.model_dump()
    department = await department_repo.create(department_dict)

    return department

@department_router.get('/department/', response_model=List[DepatmentRead])
async def get_all_department(db_session: AsyncSession = Depends(get_async_session)):
    department = DepartmentRepository(db_session=db_session)
    result = await department.get_all()
    return result
