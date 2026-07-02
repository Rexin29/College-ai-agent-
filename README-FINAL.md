# College Syllabus & Notes AI Assistant

**A full-stack Retrieval-Augmented Generation (RAG) system for college education**

![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen)
![Node](https://img.shields.io/badge/node-16%2B-brightgreen)

## 🎯 Overview

An AI-powered assistant that answers questions about college syllabus and study materials using state-of-the-art Retrieval-Augmented Generation (RAG) technology. The system retrieves relevant information from uploaded documents and generates accurate, contextual answers with source citations.

## ✨ Key Features

- 🤖 **AI-Powered Chat**: Ask questions, get instant answers with source citations
- 📚 **Multi-Format Support**: PDF, DOCX, PPTX, TXT, CSV, XLSX, Markdown, HTML, Images (OCR)
- 🔍 **Semantic Search**: Vector-based similarity search using ChromaDB
- 🏫 **Metadata Filtering**: Filter by department, year, semester, subject
- 🚀 **Local LLMs**: Powered by Ollama (Llama 3.2, Mistral, Gemma, Qwen)
- 💾 **Vector Database**: ChromaDB for efficient semantic storage and retrieval
- 👥 **Admin Panel**: Upload, manage, and delete documents
- 🎨 **Modern UI**: React frontend with dark/light mode, responsive design
- 🔐 **No Hallucinations**: Only answers from uploaded documents
- 📱 **Mobile Friendly**: Works on all devices
- 🐳 **Docker Ready**: Full Docker Compose setup

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                   React Frontend                │
│              (Chat, Admin, Settings)            │
└────────────────┬────────────────────────────────┘
                 │ REST API
┌────────────────▼────────────────────────────────┐
│              FastAPI Backend                    │
│  ┌────────────────────────────────────────┐    │
│  │      Document Processing Pipeline      │    │
│  │  (PDF, DOCX, PPTX, TXT, CSV, etc.)    │    │
│  └────────────────┬───────────────────────┘    │
│                   │                             │
│  ┌────────────────▼───────────────────────┐    │
│  │      RAG Pipeline                       │    │
│  │  - Embedding Generation                │    │
│  │  - Semantic Retrieval                  │    │
│  │  - LLM Response Generation             │    │
│  └────────────────┬───────────────────────┘    │
│                   │                             │
│  ┌────────────────▼───────────────────────┐    │
│  │      Vector Database (ChromaDB)         │    │
│  │  - Semantic Storage                    │    │
│  │  - Similarity Search                   │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼────────┐
│  Ollama (LLM)  │   │  Ollama (Embed) │
│  - llama3.2    │   │ - mxbai-embed   │
│  - mistral     │   │ - nomic-embed   │
│  - gemma       │   └─────────────────┘
│  - qwen        │
└────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Ollama
- Git

### 1. Clone Repository

```bash
git clone https://github.com/Rexin29/College-ai-agent-.git
cd College-ai-agent-
```

### 2. Install Ollama Models

```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
ollama serve
```

### 3. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

**Backend**: http://localhost:8000

### 4. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

**Frontend**: http://localhost:5173

### 5. Use the Application

1. Open http://localhost:5173
2. Go to **Admin Panel**
3. Upload a PDF/DOCX document
4. Go to **Chat**
5. Ask a question!

## 🐳 Docker Quick Start

```bash
git clone https://github.com/Rexin29/College-ai-agent-.git
cd College-ai-agent-

# Build and start
docker-compose up --build

# In another terminal, pull models
docker exec college-rag-ollama ollama pull llama3.2
docker exec college-rag-ollama ollama pull mxbai-embed-large
```

Access:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup instructions for local and Docker deployment
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- **[backend/README.md](backend/README.md)** - Backend API documentation
- **[frontend/README.md](frontend/README.md)** - Frontend documentation

## 🎯 Query Examples

After uploading documents, try:

- "What is normalization in DBMS?"
- "Explain Unit 3 concepts"
- "Give me important exam topics"
- "What's covered in Semester 5?"
- "Compare Stack and Queue"
- "Summarize Chapter 2"
- "What are the learning objectives?"

## 📁 Project Structure

```
College-ai-agent-/
├── backend/
│   ├── api/                    # FastAPI routes
│   ├── rag/                    # RAG pipeline
│   ├── vector_db/              # ChromaDB integration
│   ├── document_processor/     # File processing
│   ├── utils/                  # Configuration, logging
│   ├── main.py                 # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── hooks/              # Custom hooks
│   │   ├── services/           # API service
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── README.md
├── docker-compose.yml
├── SETUP.md
├── DEPLOYMENT.md
└── README.md
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
UPLOAD_DIR=./uploads

# RAG
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5

# API
API_PORT=8000
ALLOWED_ORIGINS=http://localhost:5173
```

## 🛠️ API Endpoints

### Health
- `GET /api/health` - Health check

### Documents
- `POST /api/upload` - Upload document
- `GET /api/documents` - List documents
- `DELETE /api/documents/{id}` - Delete document
- `POST /api/documents/reindex` - Rebuild index

### Chat
- `POST /api/chat` - Ask question
- `GET /api/chat/history/{id}` - Get conversation
- `DELETE /api/chat/history/{id}` - Clear conversation

## 🤝 Supported Models

### LLMs
- Llama 3.2 (default)
- Mistral
- Gemma
- Qwen
- Neural Chat

### Embeddings
- mxbai-embed-large (default)
- nomic-embed-text
- all-MiniLM-L6-v2
- bge-small-en-v1.5

## 🔐 Security

- ✅ Input validation on all endpoints
- ✅ File type and size validation
- ✅ No API keys required (local operation)
- ✅ Secure file storage
- ✅ Error handling without stack traces
- ✅ CORS configuration

## 🐛 Troubleshooting

### Ollama Connection Error
```bash
ollama serve  # In another terminal
```

### Models Not Found
```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
```

### Port Already in Use
```bash
# Change port in .env
API_PORT=8001
```

See [SETUP.md](SETUP.md#-troubleshooting) for more troubleshooting steps.

## 📈 Performance

- **Embedding**: ~100ms per query
- **Retrieval**: ~50ms for top-5 documents
- **Generation**: ~1-5s depending on answer length
- **Total**: ~2-7s per query (first-run slower)

## 🚀 Future Enhancements

- [ ] Hybrid search (keyword + vector)
- [ ] User authentication & authorization
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Batch processing
- [ ] API rate limiting
- [ ] WebSocket support for streaming responses
- [ ] Document versioning
- [ ] Advanced caching strategies
- [ ] Fine-tuning support

## 📄 Technology Stack

**Backend**
- FastAPI - Web framework
- LangChain - RAG orchestration
- ChromaDB - Vector database
- Ollama - Local LLM runtime
- Sentence Transformers - Embeddings
- PyPDF2/pdfplumber - PDF processing
- python-docx - DOCX processing
- python-pptx - PPTX processing

**Frontend**
- React 18 - UI framework
- Vite - Build tool
- Tailwind CSS - Styling
- Axios - HTTP client
- React Router - Navigation
- Lucide React - Icons

**Infrastructure**
- Docker - Containerization
- Docker Compose - Orchestration

## 📖 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support & Issues

- 🐛 [Report Bug](https://github.com/Rexin29/College-ai-agent-/issues)
- 💡 [Request Feature](https://github.com/Rexin29/College-ai-agent-/issues)
- 💬 [Discussions](https://github.com/Rexin29/College-ai-agent-/discussions)

## 📺 Demo

See [SETUP.md](SETUP.md) to get started!

## 🙏 Acknowledgments

- Ollama team for local LLM runtime
- LangChain for RAG framework
- ChromaDB for vector storage
- OpenAI for inspiration
- All contributors and users

---

**Made with ❤️ for students and educators**
