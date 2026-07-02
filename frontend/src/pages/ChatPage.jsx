import React from 'react'
import { useChat } from '../hooks/useChat'
import Message from '../components/Message'
import { Send, Plus, Trash2 } from 'lucide-react'

function ChatPage() {
  const { messages, loading, error, sendMessage, clearMessages } = useChat()
  const [input, setInput] = React.useState('')
  const messagesEndRef = React.useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  React.useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async (e) => {
    e.preventDefault()
    if (input.trim()) {
      await sendMessage(input)
      setInput('')
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Chat Container */}
      <div className="flex-1 overflow-auto p-4 md:p-6">
        <div className="max-w-4xl mx-auto">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-center">
              <div className="text-6xl mb-4">🎓</div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                Welcome to College RAG Assistant
              </h2>
              <p className="text-gray-600 dark:text-gray-400 max-w-md mb-6">
                Ask questions about your uploaded syllabus and study materials. The AI will search
                through your documents and provide accurate answers with citations.
              </p>
              <div className="space-y-2 text-left">
                <p className="font-semibold text-gray-700 dark:text-gray-300">Try asking:</p>
                <ul className="text-gray-600 dark:text-gray-400 space-y-1">
                  <li>• What is normalization in DBMS?</li>
                  <li>• Explain Unit 3 concepts</li>
                  <li>• Give important exam topics</li>
                  <li>• What's covered in Semester 5?</li>
                </ul>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <Message key={message.id} message={message} />
          ))}

          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-4">
              <p className="text-red-700 dark:text-red-200">{error}</p>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4 md:p-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center space-x-2 mb-4">
            {messages.length > 0 && (
              <button
                onClick={clearMessages}
                className="flex items-center space-x-1 px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-smooth"
              >
                <Trash2 size={16} />
                <span>Clear</span>
              </button>
            )}
          </div>

          <form onSubmit={handleSend} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about your syllabus or notes..."
              disabled={loading}
              className="input-base flex-1 disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="btn-primary px-4 flex items-center space-x-2 disabled:opacity-50"
            >
              <Send size={18} />
            </button>
          </form>

          <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
            💡 Tip: Be specific in your questions for better answers
          </p>
        </div>
      </div>
    </div>
  )
}

export default ChatPage
