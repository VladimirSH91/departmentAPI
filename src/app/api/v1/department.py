from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from schemes import DepatmentCreate, DepatmentRead, EmployeeCreate, DepartmentUpdate
from repositories.department import DepartmentRepository
from repositories.employee import EmployeeRepository
from service.department import DepartmentService
from service.employee import EmployeeService
from db.database import get_async_session

department_router = APIRouter()


@department_router.post('/department/', status_code=200)
async def add_depatment(data: DepatmentCreate, 
                        db_session: AsyncSession = Depends(get_async_session)):
    async with db_session.begin():
        department_repo = DepartmentRepository(db_session=db_session)
        employee_repo = EmployeeRepository(db_session=db_session)
        service = DepartmentService(repo=department_repo, employee_repo=employee_repo)
        department = await service.create_department(data)

    return department


@department_router.get('/department/')
async def get_all_department(db_session: AsyncSession = Depends(get_async_session)):
    """Функция не предусмотрена ТЗ, однако позволяет просмотреть все созданные в БД записи"""
    department = DepartmentRepository(db_session=db_session)
    result = await department.get_all()

    return result


@department_router.post('/departments/{id}/employees/', status_code=200)
async def add_employee(data: EmployeeCreate,
                       db_session: AsyncSession = Depends(get_async_session)):
    async with db_session.begin():
        employee_repo = EmployeeRepository(db_session=db_session)
        department_repo = DepartmentRepository(db_session=db_session)
        service = EmployeeService(employee_repo=employee_repo, department_repo=department_repo)
        result = await service.add_employee(data)
    return result


@department_router.get('/department/{id}', status_code=200)
async def get_depatment_by_id(id: int,
                              dept: int, 
                              include_employees: bool, 
                              sort_employees_by: str,
                              db_session: AsyncSession = Depends(get_async_session)):
    repository = DepartmentRepository(db_session=db_session)
    employee_repo = EmployeeRepository(db_session=db_session)
    department_servise = DepartmentService(repo=repository, employee_repo=employee_repo)
    result = await department_servise.get_department_tree(department_id=id, 
                                                   dept=dept,
                                                   include_employees=include_employees,
                                                   sort_employees_by=sort_employees_by)

    if not result:
        raise HTTPException(status_code=404, detail="Department not found")

    return result


@department_router.patch('/departments/{id}', status_code=200)
async def department_update(department_id: int,
                            data: DepartmentUpdate,
                            db_session: AsyncSession = Depends(get_async_session)):
    department_repo = DepartmentRepository(db_session=db_session)
    servise = DepartmentService(department_repo)
    result = await servise.update_department(department_id=department_id, 
                                             update_data=data)
    return result


@department_router.delete('/departments/{id}', status_code=204)
async def delele_department(department_id: int,
                            mode: str = Query(..., pattern="^(cascade|reassign)$"),
                            reassign_to_department_id: int | None = Query(None),
                            db_session: AsyncSession = Depends(get_async_session)):
    async with db_session.begin():
        department_repo = DepartmentRepository(db_session=db_session)
        employee_repo = EmployeeRepository(db_session=db_session)
        service = DepartmentService(repo=department_repo, employee_repo=employee_repo)
        await service.delete_department(department_id=department_id,
                                        mode=mode,
                                        reassign_to_department_id=reassign_to_department_id)
