import os
from pathlib import Path
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseModel):
    """ Application settings """
    
    # General settings
    APP_NAME: str = os.getenv("APP_NAME", "Mock API")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "Mock API using FastAPI - Team B")
    
    # Data settings
    CSV_FILE_PATH: str = os.getenv("CSV_FILE_PATH", "data/resources.csv")
    JSON_FILE_PATH: str = os.getenv("JSON_FILE_PATH", "data/sample-ereserve-data.json")
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Computed settings
    CSV_FILE_FULL_PATH: str = str(BASE_DIR / CSV_FILE_PATH)
    JSON_FILE_FULL_PATH: str = str(BASE_DIR / JSON_FILE_PATH)
    
    # Authentication settings
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    API_KEYS: List[str] = [key.strip() for key in os.getenv("API_KEYS", "").split(",") if key.strip()]
    
    # Misc settings
    JSON_API_ENDPOINTS: List[str] = [
        "/users/login",
        "/schools",
        "/units",
        "/unit-offerings",
        "/readings",
        "/reading-lists",
        "/reading-list-usages",
        "/reading-list-items",
        "/reading-list-item-usages",
        "/reading-utilisations",
        "/integration-users",
        "/teaching-sessions",
    ]
    
    class Config:
        case_sensitive = True
    
# Global settings object
settings = Settings()