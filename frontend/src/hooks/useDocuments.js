import { useState, useEffect } from 'react'
import { listDocuments, deleteDocument } from '../services/api'

export const useDocuments = () => {
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchDocuments = async () => {
    try {
      setLoading(true)
      const response = await listDocuments()
      setDocuments(response.data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const remove = async (docId) => {
    try {
      await deleteDocument(docId)
      setDocuments((prev) => prev.filter((doc) => doc.document_id !== docId))
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => {
    fetchDocuments()
  }, [])

  return { documents, loading, error, refetch: fetchDocuments, remove }
}
