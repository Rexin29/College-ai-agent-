import React from 'react'
import { Copy, Download, ExternalLink } from 'lucide-react'

function SourceCitation({ source }) {
  return (
    <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-2">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="font-semibold text-blue-900 dark:text-blue-200 text-sm">
            📄 {source.file_name}
          </p>
          <div className="mt-2 text-xs text-blue-700 dark:text-blue-300 space-y-1">
            {source.page_number && <p>Page: {source.page_number}</p>}
            {source.department && <p>Department: {source.department}</p>}
            {source.subject && <p>Subject: {source.subject}</p>}
            {source.confidence_score && (
              <p>Confidence: {(source.confidence_score * 100).toFixed(1)}%</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

function Message({ message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`${
          isUser
            ? 'bg-blue-600 text-white rounded-lg rounded-tr-none'
            : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-lg rounded-tl-none'
        } max-w-2xl p-4 fade-in`}
      >
        <p className="text-sm md:text-base leading-relaxed">{message.content}</p>
        
        {/* Sources */}
        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="mt-4 pt-4 border-t border-gray-300 dark:border-gray-600">
            <p className="text-xs font-semibold mb-2">📚 Sources:</p>
            <div className="space-y-2">
              {message.sources.map((source, idx) => (
                <SourceCitation key={idx} source={source} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Message
