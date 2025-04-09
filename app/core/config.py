import os
from pathlib import Path
from pydantic import BaseModel
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
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Computed settings
    CSV_FILE_FULL_PATH: str = str(BASE_DIR / CSV_FILE_PATH)
    
    
# Global settings object
settings = Settings()