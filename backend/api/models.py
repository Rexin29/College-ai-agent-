from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class DocumentMetadata(BaseModel):
    """Document metadata schema"""
    file_name: str
    file_type: str
    department: Optional[str] = None
    year: Optional[int] = None
    semester: Optional[int] = None
    subject: Optional[str] = None
    unit: Optional[str] = None
    chapter: Optional[str] = None
    page_number: Optional[int] = None
    upload_date: Optional[datetime] = None


class UploadResponse(BaseModel):
    """Response schema for file upload"""
    status: str
    message: str
    document_id: str
    file_name: str
    chunks_created: int
    upload_date: datetime


class DocumentInfo(BaseModel):
    """Document information schema"""
    document_id: str
    file_name: str
    file_type: str
    chunks_count: int
    metadata: Dict[str, Any]
    upload_date: datetime


class ChatMessage(BaseModel):
    """Chat message schema"""
    id: Optional[str] = None
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None
    sources: Optional[List[Dict[str, Any]]] = None


class ChatRequest(BaseModel):
    """Chat request schema"""
    question: str
    department: Optional[str] = None
    year: Optional[int] = None
    semester: Optional[int] = None
    subject: Optional[str] = None
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response schema"""
    status: str
    answer: str
    query: str
    sources: List[Dict[str, Any]]
    num_sources: int
    conversation_id: str
    timestamp: datetime


class ConversationHistory(BaseModel):
    """Conversation history schema"""
    conversation_id: str
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime


class HealthResponse(BaseModel):
    """Health check response schema"""
    status: str
    message: str
    timestamp: datetime
    components: Dict[str, str]


class ErrorResponse(BaseModel):
    """Error response schema"""
    status: str
    error: str
    message: str
    timestamp: datetime
