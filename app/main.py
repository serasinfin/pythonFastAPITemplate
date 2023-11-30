# System
import logging
# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# App
from app.core.config import settings
from app.api.api import api_router

logging.basicConfig(
    format="%(asctime)s - %(message)s", level=logging.INFO
)

logging.info(
    f"Starting server..."
)


app = FastAPI(
    title=settings.PROJECT_NAME
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)