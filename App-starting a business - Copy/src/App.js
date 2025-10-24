import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider } from './contexts/AppContext';
import Dashboard from './pages/Dashboard';
import LoadingSpinner from './components/ui/LoadingSpinner';
import MessageModal from './components/ui/MessageModal';
import './App.css';

function App() {
  return (
    <AppProvider>
      <div className="App min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        <LoadingSpinner />
        <MessageModal />
      </div>
    </AppProvider>
  );
}

export default App; 