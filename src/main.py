from motor import motor_asyncio
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from collections import defaultdict
from src.routers import user, health, todo
from src.config import BaseConfig

settings = BaseConfig()

async def lifespan(app:FastAPI):
    app.client = motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
    app.db = app.client[settings.MONGO_DATABASE]
    try:
        app.client.admin.command("ping")
        print("Connected to MongoDB")
        print(f"Database: {settings.MONGO_URI}")
        print(f"URL: {settings.MONGO_DATABASE}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
    yield
    app.client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(user.router)
app.include_router(todo.router)
app.include_router(health.router)

