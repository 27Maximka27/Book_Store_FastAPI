from fastapi import APIRouter
from src.routers.v1.books import router as books_router
from src.routers.v1.sellers import router as sellers_router
from src.routers.v1.auth import router as auth_router

router = APIRouter(prefix="/api/v1")

router.include_router(books_router)
router.include_router(sellers_router)
router.include_router(auth_router)

__all__ = ["router"]