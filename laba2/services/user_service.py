from repositories.user_repository import UserRepository
from schemas.user import UserCreate, UserUpdate

from uuid import UUID

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: UUID):
        return await self.user_repository.get_by_id(user_id)

    async def get_by_filter(self, count: int, page: int, **kwargs):
        return await self.user_repository.get_by_filter(count, page, **kwargs)

    async def create(self, user_data: UserCreate):
        return await self.user_repository.create(user_data)

    async def update(self, user_id: UUID, user_data: UserUpdate):
        return await self.user_repository.update(user_id, user_data)

    async def delete(self, user_id: UUID):
        await self.user_repository.delete(user_id)