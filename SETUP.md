# Setup Instructions for College Syllabus & Notes RAG Assistant

## 📋 Prerequisites

### Option 1: Local Setup (Recommended for Development)
- Python 3.9+
- Node.js 16+
- Ollama
- Git

### Option 2: Docker Setup (Recommended for Deployment)
- Docker
- Docker Compose

---

## 🚀 Local Setup Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/Rexin29/College-ai-agent-.git
cd College-ai-agent-
```

### Step 2: Install Ollama and Download Models

**Download Ollama**: https://ollama.ai

```bash
# Start Ollama service
ollama serve

# In another terminal, pull models
ollama pull llama3.2
ollama pull mxbai-embed-large

# Verify models are installed
ollama list
```

### Step 3: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env if needed (defaults should work)

# Run FastAPI server
python main.py
```

**Backend runs at**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

### Step 4: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend runs at**: http://localhost:5173

### Step 5: Verify Everything Works

1. Open http://localhost:5173 in your browser
2. Go to Admin Panel
3. Upload a test PDF document
4. Go to Chat
5. Ask a question about the document

---

## 🐳 Docker Setup Guide

### Prerequisites

- Install [Docker](https://docs.docker.com/get-docker/)
- Install [Docker Compose](https://docs.docker.com/compose/install/)

### Quick Start

```bash
# Clone repository
git clone https://github.com/Rexin29/College-ai-agent-.git
cd College-ai-agent-

# Build and start services
docker-compose up --build

# Wait for Ollama to download models (first run takes time)
# In another terminal, pull models:
docker exec college-rag-ollama ollama pull llama3.2
docker exec college-rag-ollama ollama pull mxbai-embed-large
```

**Services**:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Ollama: http://localhost:11434

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f ollama
```

### Rebuild After Changes

```bash
docker-compose up --build
```

---

## 🔧 Configuration

### Backend Configuration (.env)

```env
# Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.2              # Change to: mistral, gemma, qwen
EMBEDDING_MODEL=mxbai-embed-large  # Change to: nomic-embed-text, all-MiniLM-L6-v2

# Database
VECTOR_DB_PATH=./chroma_db

# File Upload
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE_MB=50

# RAG Parameters
CHUNK_SIZE=1000          # Size of text chunks
CHUNK_OVERLAP=200        # Overlap between chunks
TOP_K_RESULTS=5          # Number of documents to retrieve

# API
API_PORT=8000
DEBUG=False

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 📤 Usage Examples

### Upload Document

```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@document.pdf" \
  -F 'metadata={"department":"CSE","year":3,"semester":6,"subject":"DBMS"}'
```

### Ask Question

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is normalization in databases?",
    "department": "CSE"
  }'
```

### List Documents

```bash
curl "http://localhost:8000/api/documents"
```

### Delete Document

```bash
curl -X DELETE "http://localhost:8000/api/documents/{doc_id}"
```

---

## 🐛 Troubleshooting

### Issue: Ollama Connection Error

```
Error: Failed to connect to Ollama at http://localhost:11434
```

**Solution**:
```bash
# Verify Ollama is running
ollama serve

# Or check if it's already running
lsof -i :11434  # macOS/Linux
netstat -ano | findstr :11434  # Windows
```

### Issue: Models Not Found

```
Error: Model llama3.2 not found
```

**Solution**:
```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
ollama list
```

### Issue: Port Already in Use

**Solution**:
```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Change port in .env
API_PORT=8001
```

### Issue: Import Errors in Backend

**Solution**:
```bash
cd backend
pip install -r requirements.txt --upgrade
python -m pip install --upgrade pip
```

### Issue: Frontend Not Connecting to Backend

**Solution**:
1. Verify backend is running: `http://localhost:8000/api/health`
2. Check CORS in backend `.env`
3. Clear browser cache: `Ctrl+Shift+Del` or `Cmd+Shift+Del`

### Issue: Vector Database Issues

**Solution**:
```bash
# Clear vector database
rm -rf backend/chroma_db

# Restart backend
python main.py
```

---

## 📚 Supported File Types

- ✅ PDF (.pdf)
- ✅ Word Documents (.docx, .doc)
- ✅ PowerPoint (.pptx, .ppt)
- ✅ Text Files (.txt, .md, .html)
- ✅ Spreadsheets (.csv, .xlsx)
- ✅ Images (.jpg, .png, .jpeg) - with OCR
- ✅ ZIP folders containing multiple files

---

## 🎯 Example Queries

After uploading documents, try these questions:

1. "What is normalization in DBMS?"
2. "Explain Unit 3 concepts"
3. "Give me important exam topics"
4. "What's covered in Semester 5?"
5. "Compare Stack and Queue"
6. "What is Operating Systems?"
7. "Summarize Chapter 2"
8. "Which subject has normalization?"
9. "What are the learning objectives?"
10. "Show me syllabus for CSE"

---

## 🚀 Production Deployment

### Using Gunicorn + Uvicorn (Backend)

```bash
cd backend
pip install gunicorn uvicorn[standard]
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Using PM2 (Node.js Frontend)

```bash
npm install -g pm2
cd frontend
npm run build
pm2 start "npm run preview" --name "college-rag-frontend"
```

### Using Nginx as Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:5173;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 System Requirements

### Minimum
- CPU: 2 cores
- RAM: 4 GB
- Storage: 10 GB

### Recommended
- CPU: 4 cores
- RAM: 8 GB
- Storage: 50 GB

---

## 📝 Environment Variables

All configuration options in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| OLLAMA_BASE_URL | http://localhost:11434 | Ollama service URL |
| LLM_MODEL | llama3.2 | LLM model to use |
| EMBEDDING_MODEL | mxbai-embed-large | Embedding model |
| VECTOR_DB_PATH | ./chroma_db | Vector database location |
| UPLOAD_DIR | ./uploads | Document upload directory |
| CHUNK_SIZE | 1000 | Text chunk size |
| CHUNK_OVERLAP | 200 | Chunk overlap |
| TOP_K_RESULTS | 5 | Results per query |
| MAX_UPLOAD_SIZE_MB | 50 | Max file size |
| API_PORT | 8000 | Backend port |
| LOG_LEVEL | INFO | Logging level |

---

## 🔗 API Documentation

After starting the backend, visit:

```
http://localhost:8000/docs           # Swagger UI
http://localhost:8000/redoc          # ReDoc
```

---

## 📞 Support

For issues and questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Open a [GitHub Issue](https://github.com/Rexin29/College-ai-agent-/issues)
3. Check existing [Discussions](https://github.com/Rexin29/College-ai-agent-/discussions)

---

## 📄 License

MIT

---

## 🙏 Acknowledgments

- Ollama for local LLM runtime
- LangChain for RAG orchestration
- ChromaDB for vector storage
- React for frontend framework
- FastAPI for backend framework
