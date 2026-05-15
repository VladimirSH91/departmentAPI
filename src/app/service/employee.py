from fastapi import HTTPException

from repositories.employee import EmployeeRepository
from repositories.department import DepartmentRepository
from schemes import EmployeeCreate

class EmployeeService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.department_repo = DepartmentRepository(db_session)
        self.employee_repo = EmployeeRepository(db_session)

    async def add_employee(self, employee_data: EmployeeCreate) -> dict:
        """
        Добавляет сотрудника, проверяя существование департамента.
        Возвращает созданный объект (например, словарь или ORM-модель).
        """
        # Проверяем, существует ли департамент
        department = await self.department_repo.get_by_id(employee_data.department_id)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

        # Создаём сотрудника
        created_employee = await self.employee_repo.create(employee_data.model_dump())
        return created_employee
    