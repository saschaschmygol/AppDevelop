from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from declarative import User
from schemas.user import UserCreate, UserUpdate

from uuid import UUID

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[User]:
        stmt = select(User)
        for key, value in kwargs.items():
            if hasattr(User, key):
                stmt = stmt.where(getattr(User, key) == value)
        result = await self.session.execute(
            stmt.limit(count).offset((page - 1) * count)
        )
        return result.scalars().all()

    async def create(self, user_data: UserCreate) -> User:
        user = User(**user_data.dict())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: UUID, user_data: UserUpdate) -> User:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        for key, value in user_data.dict().items():
            setattr(user, key, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> None:
        user = await self.get_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
