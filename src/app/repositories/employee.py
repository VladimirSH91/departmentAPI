from sqlalchemy.ext.asyncio import AsyncSession

from models import Employee
from .base import BaseRepository

class EmployeeRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model=Employee)