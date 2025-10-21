from sqlalchemy import create_engine

def get_engine(connect_url):
    engine = create_engine(
        connect_url,
        echo=True  # Логирование SQL-запросов
    )
    return engine
