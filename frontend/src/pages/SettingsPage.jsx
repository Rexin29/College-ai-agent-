import React from 'react'

function SettingsPage() {
  const [settings, setSettings] = React.useState({
    topKResults: 5,
    chunkSize: 1000,
    chunkOverlap: 200,
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setSettings({ ...settings, [name]: parseInt(value) })
  }

  const handleSave = () => {
    // Save settings logic
    alert('Settings saved (local only for demo)')
  }

  return (
    <div className="p-4 md:p-6">
      <div className="max-w-2xl mx-auto">
        <div className="mb-6">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">Settings</h2>
          <p className="text-gray-600 dark:text-gray-400">Configure the RAG assistant behavior</p>
        </div>

        <div className="card-base p-6 space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Top K Results
            </label>
            <input
              type="number"
              name="topKResults"
              value={settings.topKResults}
              onChange={handleChange}
              min="1"
              max="20"
              className="input-base"
            />
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Number of documents to retrieve for each query
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Chunk Size
            </label>
            <input
              type="number"
              name="chunkSize"
              value={settings.chunkSize}
              onChange={handleChange}
              min="100"
              max="5000"
              step="100"
              className="input-base"
            />
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Size of text chunks for semantic search
            </p>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-900 dark:text-gray-100 mb-2">
              Chunk Overlap
            </label>
            <input
              type="number"
              name="chunkOverlap"
              value={settings.chunkOverlap}
              onChange={handleChange}
              min="0"
              max="1000"
              step="50"
              className="input-base"
            />
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Overlap between consecutive chunks to preserve context
            </p>
          </div>

          <button onClick={handleSave} className="btn-primary w-full">
            Save Settings
          </button>
        </div>
      </div>
    </div>
  )
}

export default SettingsPage
