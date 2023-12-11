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

    # JWT KEY ENCRYPT
    SECRET_KEY: str = os.getenv('SECRET', 'set-env-var')
    ALGORITHM = "HS256"

    # 60 minutes * 24 hours * 1 day = 1 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1

    # Allowed schedule
    # ALLOWED_SCHEDULE_START: str = '07:00:00'
    # ALLOWED_SCHEDULE_END: str = '19:00:00'

    # DB config and SqlAlchemy config
    # SQLALCHEMY_DATABASE_URI = "sqlite:///./sql-app.db"
    DB_USER: str = os.getenv('PG_USER')
    DB_PASSWORD: str = os.getenv('PG_PASSWORD')
    DB_NAME: str = os.getenv('PG_DBNAME')
    DB_HOST: str = os.getenv('PG_HOST')
    DB_PORT: str = os.getenv('PG_PORT')

    # DATABASE_URL_DO: str = os.getenv('DATABASE_URL')

    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
    )
    # SQLALCHEMY_DATABASE_URI = DATABASE_URL_DO


settings = Settings()
