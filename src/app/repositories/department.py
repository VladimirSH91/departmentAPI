from sqlalchemy.ext.asyncio import AsyncSession

from models import Department
from .base import BaseRepository

class DepartmentRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session=db_session, model=Department)
