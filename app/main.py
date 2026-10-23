from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine
from app.models.base import Base
from app.api.routers.task import router as task_router
from app.api.routers.category import router as category_router

@asynccontextmanager
async def lifespan(_:FastAPI):
    print("Запуск приложения")
    Base.metadata.create_all(bind=engine)
    yield



app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_methods=["*"]
)


app.include_router(router=task_router)
app.include_router(router=category_router)
