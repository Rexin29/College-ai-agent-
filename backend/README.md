# College Syllabus & Notes RAG Assistant

Full-stack AI assistant for college education using Retrieval-Augmented Generation.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Ollama
- Git

### Backend Setup

1. **Pull Ollama Models**
   ```bash
   ollama pull llama3.2
   ollama pull mxbai-embed-large
   ```

2. **Install Dependencies**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   ```

4. **Run Server**
   ```bash
   python main.py
   ```
   Server: http://localhost:8000
   API Docs: http://localhost:8000/docs

## 📚 API Usage Examples

### Upload Document
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@document.pdf" \
  -F "metadata={\"department\":\"CSE\",\"year\":3,\"semester\":6}"
```

### Ask Question
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is normalization in DBMS?",
    "department": "CSE",
    "year": 3
  }'
```

### List Documents
```bash
curl "http://localhost:8000/api/documents"
```

## 🎯 Features

✅ Multi-file support (PDF, DOCX, PPTX, TXT, CSV, etc.)
✅ Semantic search with vector database
✅ Local LLM powered by Ollama
✅ Source citations and confidence scores
✅ Conversation memory
✅ No hallucinations - only from uploaded documents
✅ Metadata filtering by department, year, semester, subject
✅ REST API for easy integration

## 📁 Project Structure

```
backend/
├── api/
│   ├── models.py        # Request/Response schemas
│   ├── routes.py        # API endpoints
│   └── __init__.py
├── rag/
│   ├── embeddings.py    # Embedding generation
│   ├── llm.py          # LLM interactions
│   ├── retriever.py    # RAG pipeline
│   └── __init__.py
├── vector_db/
│   ├── chroma_db.py    # Vector database
│   └── __init__.py
├── document_processor/
│   ├── pdf_processor.py
│   ├── docx_processor.py
│   ├── text_processor.py
│   ├── csv_processor.py
│   ├── pptx_processor.py
│   ├── markdown_processor.py
│   ├── document_processor.py
│   └── __init__.py
├── utils/
│   ├── config.py        # Configuration
│   ├── logger.py        # Logging setup
│   ├── validators.py    # Input validation
│   └── __init__.py
├── main.py              # FastAPI application
├── requirements.txt
└── .env.example
```

## 🔧 Configuration

Edit `.env` file:

```env
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.2
EMBEDDING_MODEL=mxbai-embed-large

# Database
VECTOR_DB_PATH=./chroma_db

# Upload
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE_MB=50

# RAG
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5

# API
API_PORT=8000
DEBUG=False

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

## 🤖 Supported Models

### LLMs
- llama3.2 (default)
- mistral
- gemma
- qwen

### Embeddings
- mxbai-embed-large (default)
- nomic-embed-text
- all-MiniLM-L6-v2

## 🛠️ Troubleshooting

### Ollama Connection Error
```bash
ollama serve
```

### Port Already in Use
```bash
python main.py --port 8001
```

### Module Import Errors
```bash
pip install -r requirements.txt --upgrade
```

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/upload` | Upload document |
| GET | `/api/documents` | List documents |
| DELETE | `/api/documents/{id}` | Delete document |
| POST | `/api/chat` | Ask question |
| GET | `/api/chat/history/{id}` | Get conversation |
| DELETE | `/api/chat/history/{id}` | Clear conversation |
| POST | `/api/documents/reindex` | Rebuild index |

## 🚀 Deployment

### Docker
```bash
docker build -t college-rag-assistant .
docker run -p 8000:8000 college-rag-assistant
```

### Production
- Use PostgreSQL/MongoDB for conversation storage
- Add authentication/authorization
- Implement rate limiting
- Use Redis for caching
- Deploy with Gunicorn/Uvicorn

## 📄 License

MIT
