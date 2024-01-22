# System
import logging
# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# App
from app.core.config import settings
from app.api.api import api_router
from app.db.init_db import init_db


logging.basicConfig(
    format="%(asctime)s - %(message)s", level=logging.INFO
)

# Init DB
logging.info(
    f"Starting db..."
)
init_db()


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
