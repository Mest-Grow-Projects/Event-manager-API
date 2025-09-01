from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    print("Application shutting down...")

app = FastAPI(
    title="Events Management API",
    description="A REST API to manage events",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return "Event Management System API"
