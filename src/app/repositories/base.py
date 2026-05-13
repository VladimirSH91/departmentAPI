from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class BaseRepository(ABC):
    def __init__(self, db_session: AsyncSession, model) -> None:
        self.db_session = db_session
        self.model = model

    async def create(self, data):
        new_md = self.model(**data)
        self.db_session.add(new_md)
        await self.db_session.flush()
        await self.db_session.refresh(new_md)
        return new_md
    
    async def get_by_id(self, id):
        return await self.db_session.get(self.model, id)
    
    async def get_all(self):
        stmt = select(self.model)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def update(self, data: dict, update_data: dict):
        for key, value in update_data.items():
            setattr(data, key, value)

        await self.db_session.flush()
        await self.db_session.refresh(data)
        return data

    async def delete(self, data) -> None:
        await self.db_session.delete(data)
        await self.db_session.flush()