import React from 'react'
import { Sun, Moon } from 'lucide-react'

function Header({ darkMode, onDarkModeToggle }) {
  return (
    <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex justify-between items-center shadow-sm">
      <div>
        <h1 className="text-2xl font-bold text-blue-600">College RAG Assistant</h1>
        <p className="text-sm text-gray-500 dark:text-gray-400">Powered by AI & Local LLMs</p>
      </div>
      <button
        onClick={onDarkModeToggle}
        className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-smooth"
      >
        {darkMode ? <Sun size={20} /> : <Moon size={20} />}
      </button>
    </header>
  )
}

export default Header
