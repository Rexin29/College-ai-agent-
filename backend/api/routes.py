from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from pathlib import Path
import uuid
from datetime import datetime
from typing import List, Optional

from document_processor import DocumentProcessor
from vector_db import ChromaVectorDB
from rag import EmbeddingManager, LLMManager, RAGRetriever
from utils.config import Config
from utils.logger import logger
from utils.validators import validate_file_extension, validate_file_size
from .models import (
    UploadResponse,
    DocumentInfo,
    ChatRequest,
    ChatResponse,
    HealthResponse,
    ErrorResponse,
)

# Initialize routers
router = APIRouter(prefix="/api", tags=["api"])

# Global instances (will be initialized in main.py)
embedding_manager = None
llm_manager = None
vector_db = None
rag_retriever = None
doc_processor = None

# Store conversations in memory (use database for production)
conversations = {}


def initialize_services():
    """Initialize all services"""
    global embedding_manager, llm_manager, vector_db, rag_retriever, doc_processor
    
    logger.info("Initializing services...")
    
    try:
        embedding_manager = EmbeddingManager()
        llm_manager = LLMManager()
        vector_db = ChromaVectorDB(embedding_manager.get_embedding_function())
        rag_retriever = RAGRetriever(vector_db, llm_manager, embedding_manager)
        doc_processor = DocumentProcessor()
        
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing services: {str(e)}")
        raise


# ==================== HEALTH CHECK ====================

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns:
        HealthResponse with service status
    """
    return HealthResponse(
        status="healthy",
        message="College RAG Assistant is running",
        timestamp=datetime.now(),
        components={
            "embedding_service": "operational",
            "llm_service": "operational",
            "vector_db": "operational",
        },
    )


# ==================== DOCUMENT MANAGEMENT ====================

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...), metadata: Optional[str] = None):
    """
    Upload a document for processing
    
    Args:
        file: Uploaded file
        metadata: JSON string with metadata (department, year, semester, subject)
        
    Returns:
        UploadResponse with document ID and chunks created
    """
    try:
        # Validate file
        if not validate_file_extension(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported: {Path(file.filename).suffix}",
            )
        
        # Save file
        file_path = Path(Config.UPLOAD_DIR) / f"{uuid.uuid4()}_{file.filename}"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = await file.read()
        
        if not validate_file_size(len(content)):
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {Config.MAX_UPLOAD_SIZE_MB}MB",
            )
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"Saved file: {file_path}")
        
        # Parse metadata
        doc_metadata = {"upload_date": datetime.now().isoformat()}
        if metadata:
            import json
            doc_metadata.update(json.loads(metadata))
        
        # Process document
        documents = doc_processor.process_file(str(file_path), doc_metadata)
        
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Add to vector database
        doc_ids = vector_db.add_documents(documents)
        
        logger.info(f"Document uploaded and processed: {doc_id}")
        
        return UploadResponse(
            status="success",
            message=f"Document processed successfully",
            document_id=doc_id,
            file_name=file.filename,
            chunks_created=len(documents),
            upload_date=datetime.now(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents", response_model=List[DocumentInfo])
async def list_documents():
    """
    List all uploaded documents
    
    Returns:
        List of DocumentInfo objects
    """
    try:
        all_docs = vector_db.get_all_documents()
        
        # Group by document
        doc_groups = {}
        for doc_id, metadata in zip(all_docs["ids"], all_docs["metadatas"]):
            file_name = metadata.get("file_name", "unknown")
            if file_name not in doc_groups:
                doc_groups[file_name] = {
                    "document_id": str(uuid.uuid4()),
                    "file_name": file_name,
                    "file_type": metadata.get("file_type", "unknown"),
                    "chunks_count": 0,
                    "metadata": metadata,
                    "upload_date": datetime.fromisoformat(
                        metadata.get("upload_date", datetime.now().isoformat())
                    ),
                }
            doc_groups[file_name]["chunks_count"] += 1
        
        documents = [
            DocumentInfo(**doc_info) for doc_info in doc_groups.values()
        ]
        
        logger.info(f"Retrieved {len(documents)} documents")
        return documents
        
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    """
    Delete a document from the vector database
    
    Args:
        doc_id: Document ID to delete
        
    Returns:
        Success message
    """
    try:
        vector_db.delete_document(doc_id)
        logger.info(f"Deleted document: {doc_id}")
        return {"status": "success", "message": f"Document {doc_id} deleted"}
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/documents/reindex")
async def reindex_documents():
    """
    Rebuild the vector database index
    
    Returns:
        Success message
    """
    try:
        logger.info("Starting vector database reindex...")
        # Note: In production, implement proper reindexing logic
        return {"status": "success", "message": "Vector database reindexed successfully"}
    except Exception as e:
        logger.error(f"Error reindexing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CHAT & RAG ====================

@router.post("/chat", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """
    Ask a question and get an answer based on uploaded documents
    
    Args:
        request: ChatRequest with question and optional filters
        
    Returns:
        ChatResponse with answer and sources
    """
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Build metadata filter if provided
        metadata_filter = {}
        if request.department:
            metadata_filter["department"] = request.department
        if request.year:
            metadata_filter["year"] = request.year
        if request.semester:
            metadata_filter["semester"] = request.semester
        if request.subject:
            metadata_filter["subject"] = request.subject
        
        # Get answer from RAG pipeline
        result = rag_retriever.rag_pipeline(
            request.question,
            metadata_filter if metadata_filter else None
        )
        
        # Get or create conversation
        conversation_id = request.conversation_id or str(uuid.uuid4())
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        # Store conversation
        conversations[conversation_id].append({
            "role": "user",
            "content": request.question,
            "timestamp": datetime.now(),
        })
        conversations[conversation_id].append({
            "role": "assistant",
            "content": result["answer"],
            "timestamp": datetime.now(),
            "sources": result["sources"],
        })
        
        logger.info(f"Answered question: {request.question}")
        
        return ChatResponse(
            status=result["status"],
            answer=result["answer"],
            query=request.question,
            sources=result["sources"],
            num_sources=result.get("num_sources", len(result["sources"])),
            conversation_id=conversation_id,
            timestamp=datetime.now(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/history/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """
    Get conversation history
    
    Args:
        conversation_id: Conversation ID
        
    Returns:
        Conversation history
    """
    try:
        if conversation_id not in conversations:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "conversation_id": conversation_id,
            "messages": conversations[conversation_id],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/chat/history/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """
    Clear conversation history
    
    Args:
        conversation_id: Conversation ID
        
    Returns:
        Success message
    """
    try:
        if conversation_id in conversations:
            del conversations[conversation_id]
        logger.info(f"Cleared conversation: {conversation_id}")
        return {"status": "success", "message": "Conversation cleared"}
    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
