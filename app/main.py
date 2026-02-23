from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import places, projects


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await conn.close()


app = FastAPI(
    title="Travel Planner API",
    lifespan=lifespan
)


app.include_router(places.router)
app.include_router(projects.router)

@app.get("/")
async def read_root():
    return {"message": "Hello"}