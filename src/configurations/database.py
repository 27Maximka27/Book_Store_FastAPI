from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.configurations.settings import settings

# Синхронный движок
engine = create_engine(
    settings.database_url,
    echo=True,
    pool_size=5,
    max_overflow=10
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Зависимость для получения сессии БД
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()