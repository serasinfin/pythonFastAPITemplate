# FastAPI imports
from fastapi import APIRouter

# App routers
from app.api.routers import hello

api_router = APIRouter()

# Include routers
api_router.include_router(hello.router, prefix="/hello", tags=["Hello"])
