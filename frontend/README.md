# College RAG Assistant - Frontend

React-based frontend for the College Syllabus & Notes RAG Assistant.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Frontend runs at http://localhost:5173

### Build for Production

```bash
npm run build
```

## 📚 Features

✅ **Chat Interface** - Ask questions about uploaded documents
✅ **Admin Panel** - Upload and manage documents
✅ **Settings** - Configure RAG parameters
✅ **Dark/Light Mode** - Toggle between themes
✅ **Responsive Design** - Works on mobile and desktop
✅ **Source Citations** - See which documents were used for answers
✅ **Conversation History** - Keep track of past questions

## 🏗️ Project Structure

```
src/
├── components/
│   ├── Header.jsx          # Top navigation bar
│   ├── Sidebar.jsx         # Side navigation
│   ├── Message.jsx         # Chat message component
│   ├── FileUpload.jsx      # Document upload
│   └── DocumentList.jsx    # List of uploaded documents
├── pages/
│   ├── ChatPage.jsx        # Main chat interface
│   ├── AdminPage.jsx       # Admin document management
│   └── SettingsPage.jsx    # Settings configuration
├── hooks/
│   ├── useChat.js          # Chat logic hook
│   ├── useDocuments.js     # Document management hook
│   └── useChatStore.js     # Zustand store for chat state
├── services/
│   └── api.js              # API client for backend
├── App.jsx                 # Main app component
├── main.jsx                # Entry point
└── index.css               # Tailwind styles
```

## 🔌 API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000/api`

### Key Endpoints

- `POST /api/upload` - Upload documents
- `GET /api/documents` - List documents
- `POST /api/chat` - Ask questions
- `GET /api/health` - Health check

## 🎨 Styling

- **Tailwind CSS** for utility-first styling
- **Dark mode support** with `dark:` prefix
- **Responsive design** with mobile-first approach
- **Custom components** with consistent styling

## 📱 Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## 🔐 Environment Variables

Create a `.env` file if needed:

```env
VITE_API_URL=http://localhost:8000/api
```

## 🚀 Deployment

### Build Static Files

```bash
npm run build
```

Output goes to `dist/` directory. Serve with any static file server:

```bash
npx serve -s dist
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "run", "preview"]
```

## 🐛 Troubleshooting

### API Connection Issues
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in backend `.env`
- Verify proxy settings in `vite.config.js`

### Styling Issues
- Clear node_modules: `rm -rf node_modules && npm install`
- Rebuild Tailwind: `npm run build`

## 📄 License

MIT
