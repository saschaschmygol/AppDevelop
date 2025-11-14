from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)  # Обязательное, с валидацией длины
    email: EmailStr  # Валидация email с помощью EmailStr
    description: Optional[str] = Field(None, max_length=500)  # Опциональное


class UserCreate(UserBase):
    pass  # Наследует все от UserBase


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    description: Optional[str] = Field(None, max_length=500)


class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Автоматическая конвертация из SQLAlchemy-модели (model_validate)

# Если нужно список для GET /users
class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int  # Для пагинации, если добавишь
    page: int
    count: int