from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from litestar.params import Parameter, Body
from litestar.exceptions import NotFoundException
from typing import List

from services.user_service import UserService
from schemas.user import UserCreate, UserUpdate, UserResponse
from uuid import UUID

class UserController(Controller):
    path = "/users"

    @get("/{user_id:uuid}")
    async def get_user_by_id(
        self, user_service: UserService, user_id: UUID
    ) -> UserResponse:
        user = await user_service.get_by_id(user_id)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @get()
    async def get_all_users(
        self, user_service: UserService, count: int = 10, page: int = 1
    ) -> List[UserResponse]:
        users = await user_service.get_by_filter(count=count, page=page)
        return [UserResponse.model_validate(u) for u in users]

    @post()
    async def create_user(
        self, user_service: UserService, data: UserCreate
    ) -> UserResponse:
        user = await user_service.create(data)
        return UserResponse.model_validate(user)

    @put("/{user_id:uuid}")
    async def update_user(
        self, user_service: UserService, user_id: UUID, data: UserUpdate
    ) -> UserResponse:
        user = await user_service.update(user_id, data)
        if not user:
            raise NotFoundException(detail=f"User with ID {user_id} not found")
        return UserResponse.model_validate(user)

    @delete("/{user_id:uuid}")
    async def delete_user(self, user_service: UserService, user_id: UUID) -> None:
        await user_service.delete(user_id)


