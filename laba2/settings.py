from pydantic_settings import BaseSettings
from pydantic import Field  # Field для валидации, если нужно

class DBSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def get_sync_connect_str(self) -> str:
        """Синхронное подключение"""
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def get_async_connect_str(self) -> str:
        """Асинхронное подключение"""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
