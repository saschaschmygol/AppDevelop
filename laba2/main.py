from http.cookiejar import debug

from settings import DBSettings
from engine import get_engine

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from litestar import Litestar
from litestar.di import Provide

from controllers.user_controller import UserController
from repositories.user_repository import UserRepository
from services.user_service import UserService
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()
settings = DBSettings(
    host=os.getenv('POSTGRES_HOST'),
    port=os.getenv('POSTGRES_PORT'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    database=os.getenv('POSTGRES_DB'),
)

engine = get_engine(settings.get_async_connect_str)
async_session_factory = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def provide_db_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def provide_user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


async def provide_user_service(user_repository: UserRepository) -> UserService:
    return UserService(user_repository)


app = Litestar(
    route_handlers=[UserController],
    dependencies={
        "db_session": Provide(provide_db_session),
        "user_repository": Provide(provide_user_repository),
        "user_service": Provide(provide_user_service),
    },
    debug=True)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
