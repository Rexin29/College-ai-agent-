import React, { useEffect } from 'react'
import FileUpload from '../components/FileUpload'
import DocumentList from '../components/DocumentList'
import { uploadDocument } from '../services/api'
import { useDocuments } from '../hooks/useDocuments'

function AdminPage() {
  const { documents, loading, error, refetch, remove } = useDocuments()
  const [uploading, setUploading] = React.useState(false)
  const [uploadError, setUploadError] = React.useState(null)
  const [uploadSuccess, setUploadSuccess] = React.useState(false)

  const handleUpload = async (file, metadata) => {
    try {
      setUploading(true)
      setUploadError(null)
      setUploadSuccess(false)

      await uploadDocument(file, metadata)
      setUploadSuccess(true)
      await refetch()

      setTimeout(() => setUploadSuccess(false), 3000)
    } catch (err) {
      setUploadError(err.response?.data?.detail || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="p-4 md:p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">Admin Panel</h2>
          <p className="text-gray-600 dark:text-gray-400">Manage your documents and study materials</p>
        </div>

        {uploadSuccess && (
          <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
            <p className="text-green-700 dark:text-green-200">✓ Document uploaded successfully!</p>
          </div>
        )}

        {uploadError && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <p className="text-red-700 dark:text-red-200">{uploadError}</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <p className="text-red-700 dark:text-red-200">{error}</p>
          </div>
        )}

        <FileUpload onUpload={handleUpload} loading={uploading} />
        <DocumentList documents={documents} loading={loading} onDelete={remove} />
      </div>
    </div>
  )
}

export default AdminPage
