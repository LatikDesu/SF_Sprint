from logging.config import dictConfig

import sqlalchemy
from fastapi import FastAPI

from app.db_connection import DATABASE_URL, database
from app.routers import pereval
from app.logger import LogConfig

dictConfig(LogConfig().dict())

app = FastAPI(
    title="FSTR Pereval API",
    description="API ФСТР, предназначено для спортивно-туристического мобильного приложения.",
    contact={"name": "Evgeny Abrosimov",
             "url": "https://github.com/", },
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc", )

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(pereval.router)
