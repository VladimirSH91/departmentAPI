from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from schemes import DepatmentCreate, DepatmentRead, EmployeeCreate
from repositories.department import DepartmentRepository
from repositories.employee import EmployeeRepository
from db.database import get_async_session

department_router = APIRouter()

@department_router.post('/department/', status_code=200)
async def add_depatment(data: DepatmentCreate, 
                        db_session: AsyncSession = Depends(get_async_session)):
    # @todo тут и далее перенести в сервисный слой все обращения к БД
    async with db_session.begin():
        department_repo = DepartmentRepository(db_session=db_session)
        department_dict = data.model_dump()
        department = await department_repo.create(department_dict)

    return department

@department_router.get('/department/')
async def get_all_department(db_session: AsyncSession = Depends(get_async_session)):
    """Функция не предусмотрена ТЗ, однако позволяет просмотреть все созданные в БД записи"""
    department = DepartmentRepository(db_session=db_session)
    result = await department.get_all()

    return result

@department_router.post('/departments/{id}/employees/')
async def add_employee(data: EmployeeCreate,
                       db_session: AsyncSession = Depends(get_async_session)):
    
    async with db_session.begin():
        department_repo = DepartmentRepository(db_session=db_session)
        employee_repo = EmployeeRepository(db_session=db_session)
        employee_data = data.model_dump()
        print(employee_data)
        data_department = await department_repo.get_by_id(employee_data['department_id'])
    
        if not data_department:
            raise HTTPException(status_code=404, detail='Department not found')
    
        result = await employee_repo.create(employee_data)

    return result


@department_router.get('/department/{id}', status_code=200)
async def get_depatment_by_id(dept: int, include_employees:bool, 
                              db_session: AsyncSession = Depends(get_async_session)):
    pass
