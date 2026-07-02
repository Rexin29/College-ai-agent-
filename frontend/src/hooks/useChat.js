import { useState, useCallback } from 'react'
import { askQuestion, getConversationHistory } from '../services/api'

export const useChat = () => {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [conversationId, setConversationId] = useState(null)

  const sendMessage = useCallback(
    async (question, filters = {}) => {
      if (!question.trim()) return

      try {
        setLoading(true)
        setError(null)

        // Add user message
        const userMessage = {
          id: Date.now(),
          role: 'user',
          content: question,
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, userMessage])

        // Get response
        const response = await askQuestion(question, {
          conversation_id: conversationId,
          ...filters,
        })

        // Update conversation ID
        if (!conversationId) {
          setConversationId(response.data.conversation_id)
        }

        // Add assistant message
        const assistantMessage = {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.data.answer,
          sources: response.data.sources,
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, assistantMessage])
      } catch (err) {
        setError(err.response?.data?.detail || 'Error sending message')
      } finally {
        setLoading(false)
      }
    },
    [conversationId]
  )

  const clearMessages = useCallback(() => {
    setMessages([])
    setConversationId(null)
  }, [])

  return {
    messages,
    loading,
    error,
    conversationId,
    sendMessage,
    clearMessages,
  }
}
