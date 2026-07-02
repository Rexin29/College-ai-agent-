import React, { useState } from 'react'
import { Upload, X, Plus } from 'lucide-react'

function FileUpload({ onUpload, loading }) {
  const [file, setFile] = useState(null)
  const [metadata, setMetadata] = useState({
    department: '',
    year: '',
    semester: '',
    subject: '',
  })
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
    }
  }

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (file) {
      await onUpload(file, metadata)
      setFile(null)
      setMetadata({ department: '', year: '', semester: '', subject: '' })
    }
  }

  return (
    <div className="card-base p-6">
      <h3 className="text-lg font-semibold mb-4">📤 Upload Document</h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Drag and Drop Area */}
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-smooth ${
            dragActive
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/10'
              : 'border-gray-300 dark:border-gray-600'
          }`}
        >
          {file ? (
            <div className="flex items-center justify-between">
              <div className="flex-1 text-left">
                <p className="font-semibold text-gray-900 dark:text-gray-100">{file.name}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {(file.size / 1024).toFixed(2)} KB
                </p>
              </div>
              <button
                type="button"
                onClick={() => setFile(null)}
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
              >
                <X size={20} />
              </button>
            </div>
          ) : (
            <div>
              <Upload size={32} className="mx-auto mb-2 text-gray-400" />
              <p className="text-gray-600 dark:text-gray-400">
                Drag and drop a file here or click to select
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">
                Supported: PDF, DOCX, PPTX, TXT, CSV, etc.
              </p>
              <input
                type="file"
                onChange={handleChange}
                className="hidden"
                id="file-input"
              />
              <label
                htmlFor="file-input"
                className="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer transition-smooth"
              >
                Choose File
              </label>
            </div>
          )}
        </div>

        {/* Metadata */}
        {file && (
          <div className="grid grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Department (CSE, ECE, etc.)"
              value={metadata.department}
              onChange={(e) => setMetadata({ ...metadata, department: e.target.value })}
              className="input-base"
            />
            <input
              type="number"
              placeholder="Year"
              value={metadata.year}
              onChange={(e) => setMetadata({ ...metadata, year: e.target.value })}
              className="input-base"
            />
            <input
              type="number"
              placeholder="Semester"
              value={metadata.semester}
              onChange={(e) => setMetadata({ ...metadata, semester: e.target.value })}
              className="input-base"
            />
            <input
              type="text"
              placeholder="Subject"
              value={metadata.subject}
              onChange={(e) => setMetadata({ ...metadata, subject: e.target.value })}
              className="input-base"
            />
          </div>
        )}

        {/* Submit Button */}
        {file && (
          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full flex items-center justify-center space-x-2"
          >
            <Plus size={18} />
            <span>{loading ? 'Uploading...' : 'Upload Document'}</span>
          </button>
        )}
      </form>
    </div>
  )
}

export default FileUpload
