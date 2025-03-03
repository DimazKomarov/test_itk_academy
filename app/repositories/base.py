from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        result = res.scalar_one()
        return result

    async def find_one_or_none(self, **filter_by: dict) -> Any | None:
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        result = res.scalar_one_or_none()
        return result
