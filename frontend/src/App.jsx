import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'

// Basic placeholder component for now
const Dashboard = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6 text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-4">
        Kenyan Payroll Management System
      </h1>
      <p className="text-gray-600 mb-4">
        Welcome to the payroll management system. The application is running successfully!
      </p>
      <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
        ✅ Docker build completed successfully
      </div>
    </div>
  </div>
)

const Login = () => (
  <div className="min-h-screen bg-gray-50 flex items-center justify-center">
    <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 text-center mb-4">
        Login
      </h2>
      <p className="text-gray-600 text-center">
        Login functionality will be implemented here.
      </p>
    </div>
  </div>
)

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </div>
  )
}

export default App
