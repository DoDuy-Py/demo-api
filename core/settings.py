# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import List

load_dotenv()
print(f"-----------{os.getenv('DATABASE_URL')}------")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = os.getenv("SECRET_KEY", "123456")

class Settings():
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'FASTAPI BASE')
    VERSION = os.getenv('VERSION', '1.0.0')
    SECRET_KEY = SECRET_KEY
    API_PREFIX = ''
    BACKEND_CORS_ORIGINS: List[str] = ['*']
    DATABASE_URL = os.getenv('DATABASE_URL', '')
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Token expired after 7 days
    SECURITY_ALGORITHM = 'HS256'
    # LOGGING_CONFIG_FILE = os.path.join(BASE_DIR, 'logging.ini')


settings = Settings()