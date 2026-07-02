from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from contextlib import asynccontextmanager
import uvicorn

from api import router, initialize_services
from utils.config import Config
from utils.logger import logger


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    # Startup
    logger.info("Starting College RAG Assistant...")
    try:
        initialize_services()
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down College RAG Assistant...")


# Create FastAPI app
app = FastAPI(
    title="College Syllabus & Notes RAG Assistant",
    description="An AI-powered assistant that answers questions based on college syllabus and study materials",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZIP compression
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Include routers
app.include_router(router)


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint
    
    Returns:
        Welcome message
    """
    return {
        "message": "Welcome to College Syllabus & Notes RAG Assistant",
        "docs": "/docs",
        "health": "/api/health",
    }


if __name__ == "__main__":
    logger.info(f"Starting server on {Config.API_HOST}:{Config.API_PORT}")
    logger.info(f"Debug mode: {Config.DEBUG}")
    logger.info(f"LLM Model: {Config.LLM_MODEL}")
    logger.info(f"Embedding Model: {Config.EMBEDDING_MODEL}")
    
    uvicorn.run(
        "main:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=Config.DEBUG,
        log_level=Config.LOG_LEVEL.lower(),
    )
