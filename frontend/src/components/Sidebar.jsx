import React from 'react'
import { Link } from 'react-router-dom'
import { Menu, X, MessageSquare, Settings, Shield } from 'lucide-react'

function Sidebar({ open, onToggle }) {
  return (
    <>
      {/* Toggle Button */}
      <button
        onClick={onToggle}
        className="md:hidden fixed top-20 left-4 z-50 p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg"
      >
        {open ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar */}
      <aside
        className={`${
          open ? 'w-64' : 'w-0'
        } bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 overflow-hidden transition-all duration-300 flex flex-col`}
      >
        <nav className="p-6 space-y-4 flex-1">
          <Link
            to="/"
            className="flex items-center space-x-3 px-4 py-2 rounded-lg hover:bg-blue-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 transition-smooth"
          >
            <MessageSquare size={20} />
            <span>Chat</span>
          </Link>
          <Link
            to="/admin"
            className="flex items-center space-x-3 px-4 py-2 rounded-lg hover:bg-blue-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 transition-smooth"
          >
            <Shield size={20} />
            <span>Admin Panel</span>
          </Link>
          <Link
            to="/settings"
            className="flex items-center space-x-3 px-4 py-2 rounded-lg hover:bg-blue-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200 transition-smooth"
          >
            <Settings size={20} />
            <span>Settings</span>
          </Link>
        </nav>
      </aside>
    </>
  )
}

export default Sidebar
