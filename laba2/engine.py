from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

def get_engine(connect_url):
    engine = create_async_engine(
        connect_url,
        echo=True  # Логирование SQL-запросов
    )
    return engine
