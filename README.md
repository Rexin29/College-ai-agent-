# College Syllabus & Notes AI Assistant

A full-stack AI-powered assistant that answers questions about college syllabus and study materials using Retrieval-Augmented Generation (RAG).

## 🎯 Features

- ✅ **Semantic Search**: Retrieve relevant information from uploaded syllabus and notes
- ✅ **Multi-File Support**: PDF, DOCX, TXT, PPTX, CSV, XLSX, Markdown, HTML, Images (OCR)
- ✅ **Vector Database**: ChromaDB with semantic similarity search
- ✅ **Local LLM**: Powered by Ollama (Llama 3.2, Mistral, etc.)
- ✅ **Admin Panel**: Upload, update, delete documents
- ✅ **Source Citations**: Answers include document source and page number
- ✅ **Conversation Memory**: Maintain chat history for follow-up questions
- ✅ **No Hallucination**: Only answers from uploaded documents
- ✅ **Responsive UI**: React frontend with dark/light mode
- ✅ **REST APIs**: FastAPI backend for all operations

## 📋 Supported Query Types

- What is Unit 3?
- Explain Operating Systems
- Give important DBMS topics
- What are the exam topics?
- Show AI syllabus
- What is taught in Semester 5?
- Explain this topic in simple words
- Summarize Unit 2
- Which subject contains normalization?
- Compare Stack and Queue

## 🏗️ Project Structure

```
College-ai-agent-/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── models.py
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── retriever.py
│   │   ├── embeddings.py
│   │   └── llm.py
│   ├── vector_db/
│   │   ├── __init__.py
│   │   └── chroma_db.py
│   ├── document_processor/
│   │   ├── __init__.py
│   │   ├── pdf_processor.py
│   │   ├── docx_processor.py
│   │   ├── pptx_processor.py
│   │   ├── text_processor.py
│   │   └── ocr_processor.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── validators.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat.jsx
│   │   │   ├── FileUpload.jsx
│   │   │   ├── DocumentList.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── Header.jsx
│   │   ├── pages/
│   │   │   ├── ChatPage.jsx
│   │   │   ├── AdminPage.jsx
│   │   │   └── SettingsPage.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── hooks/
│   │   │   └── useChat.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── uploads/
├── chroma_db/
├── .env.example
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- Ollama (for local LLM)
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rexin29/College-ai-agent-.git
   cd College-ai-agent-
   ```

2. **Install Ollama models**
   ```bash
   ollama pull llama3.2
   ollama pull mxbai-embed-large
   # or
   ollama pull mistral
   ollama pull nomic-embed-text
   ```

3. **Setup Python environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run FastAPI server**
   ```bash
   python main.py
   # Server runs at http://localhost:8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   # Frontend runs at http://localhost:5173
   ```

## 📡 API Endpoints

### Documents
- `POST /api/upload` - Upload document
- `GET /api/documents` - List all documents
- `DELETE /api/documents/{doc_id}` - Delete document
- `POST /api/documents/reindex` - Rebuild vector index

### Chat
- `POST /api/chat` - Ask a question
- `POST /api/chat/history` - Get chat history
- `DELETE /api/chat/history` - Clear history

### Health
- `GET /api/health` - Server status

## 🔧 Configuration

### Backend (.env)
```
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.2
EMBEDDING_MODEL=mxbai-embed-large
VECTOR_DB_PATH=./chroma_db
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=50
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
LOG_LEVEL=INFO
```

## 📚 Document Processing

The system automatically:
1. Extracts text from various file formats
2. Cleans and formats content
3. Detects headings and sections
4. Splits into semantic chunks
5. Generates embeddings
6. Stores in vector database with metadata

### Metadata Stored
- Department
- Year
- Semester
- Subject
- Unit/Chapter
- File name
- Page number
- Upload date

## 🤖 RAG Workflow

```
User Question → Embedding → Vector Search → Retrieve Top-K Chunks → Build Prompt → LLM → Answer + Sources
```

## 💡 AI Behavior Rules

- ✅ Never hallucinate
- ✅ Only answer from retrieved documents
- ✅ Provide source citations
- ✅ If insufficient info: "I couldn't find enough information in the uploaded syllabus or notes."
- ✅ Step-by-step explanations
- ✅ Simple language for concepts
- ✅ Examples from notes when available
- ✅ Maintain conversation context

## 🔌 Supported Models

### LLMs
- Llama 3.2
- Mistral
- Gemma
- Qwen
- Neural Chat

### Embedding Models
- mxbai-embed-large (default)
- nomic-embed-text
- all-MiniLM-L6-v2
- bge-small-en-v1.5

## 📦 Technology Stack

### Backend
- **FastAPI** - Web framework
- **LangChain** - RAG orchestration
- **ChromaDB** - Vector database
- **Ollama** - Local LLM runtime
- **PyPDF2/pdfplumber** - PDF processing
- **python-docx** - DOCX processing
- **pytesseract** - OCR for images
- **Sentence Transformers** - Embeddings

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **React Router** - Navigation

## 🛠️ Admin Features

- Upload documents (single or bulk)
- View uploaded files with metadata
- Delete documents
- Rebuild embeddings
- Monitor vector DB status
- View chat analytics

## 👨‍🎓 Student Features

- Ask syllabus questions
- Search across all uploaded materials
- View answer sources
- Copy/download answers as PDF
- Maintain chat history
- Filter by department/semester

## 🔒 Security

- Input validation on all endpoints
- File type validation
- File size limits
- Rate limiting (future)
- Error handling without exposing stack traces
- Secure file storage

## 📊 Future Enhancements

- [ ] Hybrid search (keyword + vector)
- [ ] Multi-language support
- [ ] User authentication
- [ ] Role-based access control
- [ ] Advanced analytics
- [ ] Conversation export
- [ ] API rate limiting
- [ ] Batch question processing

## 🐛 Troubleshooting

### Ollama not connecting
```bash
# Start Ollama service
ollama serve
```

### Models not found
```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
```

### CORS issues
Ensure CORS is configured in `main.py`

### Port already in use
```bash
# Change port in .env or main.py
uvicorn main:app --port 8001
```

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open a GitHub issue.
