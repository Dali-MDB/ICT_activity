from fastapi import FastAPI
from .auth import auth_router
from app.end_points.ideas import ideas_router
from app.end_points.thumbs import thumbs_router
from app.db import Base, engine
from app import models
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

    
app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(ideas_router)
app.include_router(thumbs_router)