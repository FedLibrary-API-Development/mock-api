import sys
from loguru import logger
from .config import settings

# Configure logger
logger.remove()     # remove default handlers
logger.add(
    sys.stderr,
    level=settings.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

# Add file logging
logger.add(
    "logs/api.log",
    rotation="10 MB",
    retention="7 days",
    level=settings.LOG_LEVEL,
    compression="zip",
)