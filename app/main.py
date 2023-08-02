from logging.config import dictConfig

import sqlalchemy
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.db_connection import DATABASE_URL, database
from app.logger import LogConfig
from app.routers import submitdata

dictConfig(LogConfig().dict())

app = FastAPI(
    title="FSTR Pereval API",
    description="API ФСТР, предназначено для спортивно-туристического мобильного приложения.",
    contact={"name": "Evgeny Abrosimov",
             "url": "https://github.com/LatikDesu/SF_Sprint"},
    version="0.1.0",
    docs_url="/docs")

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(submitdata.router)
