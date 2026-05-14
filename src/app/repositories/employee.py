from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Employee
from .base import BaseRepository

class EmployeeRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model=Employee)

    async def get_employees(self, department_id: int, sort_by: str = "created_at"):
        if sort_by == 'full_name':
            order = Employee.full_name
        else:
            order = Employee.created_at    
        result = await self.db_session.execute(select(Employee).
                                               where(Employee.department_id == department_id).
                                               order_by(order))
        return result.scalars().all()
    