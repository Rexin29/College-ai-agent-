import logging
import logging.handlers
from pathlib import Path
from pythonjsonlogger import jsonlogger
from .config import Config


def setup_logger(name: str = "college_rag_assistant") -> logging.Logger:
    """Setup logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))

    # Create logs directory
    Path(Config.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

    # File handler with JSON format
    file_handler = logging.handlers.RotatingFileHandler(
        Config.LOG_FILE, maxBytes=10485760, backupCount=10
    )
    file_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
    file_formatter = jsonlogger.JsonFormatter()
    file_handler.setFormatter(file_formatter)

    # Console handler with standard format
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Create global logger
logger = setup_logger()
