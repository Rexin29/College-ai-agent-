import React from 'react'
import { Trash2, FileText } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'

function DocumentList({ documents, loading, onDelete }) {
  if (loading) {
    return (
      <div className="card-base p-6">
        <div className="animate-pulse space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-12 bg-gray-200 dark:bg-gray-700 rounded"></div>
          ))}
        </div>
      </div>
    )
  }

  if (!documents.length) {
    return (
      <div className="card-base p-6 text-center">
        <FileText size={32} className="mx-auto text-gray-400 mb-2" />
        <p className="text-gray-500 dark:text-gray-400">No documents uploaded yet</p>
      </div>
    )
  }

  return (
    <div className="card-base overflow-hidden">
      <div className="p-6">
        <h3 className="text-lg font-semibold mb-4">📚 Uploaded Documents ({documents.length})</h3>
        <div className="space-y-2">
          {documents.map((doc) => (
            <div
              key={doc.document_id}
              className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-smooth"
            >
              <div className="flex-1">
                <p className="font-medium text-gray-900 dark:text-gray-100">{doc.file_name}</p>
                <div className="flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400 mt-1">
                  <span>📄 {doc.file_type.toUpperCase()}</span>
                  <span>📝 {doc.chunks_count} chunks</span>
                  {doc.metadata?.department && <span>🏢 {doc.metadata.department}</span>}
                </div>
              </div>
              <button
                onClick={() => onDelete(doc.document_id)}
                className="p-2 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-smooth"
                title="Delete document"
              >
                <Trash2 size={18} />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default DocumentList
