from fastapi import FastAPI, Depends  
from sqlalchemy.orm import Session
from src.configurations.database import engine, get_db  
from src.models.base import Base
from src.routers.v1 import router as v1_router


# Создание таблиц (синхронно)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Store API", 
    description="Platform for selling books",
    version="1.0.0"
)

# Include routers
app.include_router(v1_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Book Store API", 
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Проверка подключения к БД
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}