import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import ChatPage from './pages/ChatPage'
import AdminPage from './pages/AdminPage'
import SettingsPage from './pages/SettingsPage'

function App() {
  const [darkMode, setDarkMode] = React.useState(false)
  const [sidebarOpen, setSidebarOpen] = React.useState(true)

  return (
    <Router>
      <div className={`flex h-screen ${darkMode ? 'dark' : ''}`}>
        <Sidebar open={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />
        <div className="flex flex-col flex-1">
          <Header darkMode={darkMode} onDarkModeToggle={() => setDarkMode(!darkMode)} />
          <main className="flex-1 overflow-auto bg-gray-50 dark:bg-gray-950">
            <Routes>
              <Route path="/" element={<ChatPage />} />
              <Route path="/admin" element={<AdminPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  )
}

export default App
