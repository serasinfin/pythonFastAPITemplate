# System
import os
# DotEnv
from dotenv import load_dotenv


class Settings:
    """Initialize settings"""
    # Load env vars
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'FastAPI')


settings = Settings()
