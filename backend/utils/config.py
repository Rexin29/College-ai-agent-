import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for the College RAG Assistant"""

    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "mxbai-embed-large")

    # Database
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./chroma_db")
    COLLECTION_NAME = "college_materials"

    # File Upload
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
    ALLOWED_EXTENSIONS = os.getenv(
        "ALLOWED_EXTENSIONS", "pdf,docx,txt,pptx,csv,xlsx,md,html,jpg,png,jpeg"
    ).split(",")

    # RAG Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))

    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # CORS
    ALLOWED_ORIGINS = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000"
    ).split(",")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

    # Create necessary directories
    @staticmethod
    def setup_directories():
        """Create necessary directories if they don't exist"""
        directories = [
            Config.UPLOAD_DIR,
            Config.VECTOR_DB_PATH,
            Path(Config.LOG_FILE).parent,
        ]
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)


# Setup directories on import
Config.setup_directories()
