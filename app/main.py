import sqlalchemy
from fastapi import FastAPI

from app.db_connection import DATABASE_URL, database

app = FastAPI(
    title="FSTR Pereval API",
    description="The graphic novel API for the RSHB hackathon is a set of tools and interfaces that allow "
                "you to create and run interactive stories in graphic novel format. ",
    contact={"name": "Evgeny Abrosimov",
             "url": "https://github.com/", },
    version="0.1.0",
    docs_url="/docs",
    redoc_url=None,
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
