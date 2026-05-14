from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Department
from .base import BaseRepository

class DepartmentRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model=Department)

    async def get_children(self, department_id: int):
        result = await self.db_session.execute(
            select(Department).where(Department.parent_id == department_id)
        )
        
        return result.scalars()

    