import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Health check
export const checkHealth = async () => {
  return api.get('/health')
}

// Document management
export const uploadDocument = async (file, metadata = {}) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('metadata', JSON.stringify(metadata))
  return api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const listDocuments = async () => {
  return api.get('/documents')
}

export const deleteDocument = async (docId) => {
  return api.delete(`/documents/${docId}`)
}

export const reindexDocuments = async () => {
  return api.post('/documents/reindex')
}

// Chat
export const askQuestion = async (question, filters = {}) => {
  return api.post('/chat', {
    question,
    ...filters,
  })
}

export const getConversationHistory = async (conversationId) => {
  return api.get(`/chat/history/${conversationId}`)
}

export const clearConversation = async (conversationId) => {
  return api.delete(`/chat/history/${conversationId}`)
}

export default api
