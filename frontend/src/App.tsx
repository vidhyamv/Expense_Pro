import React from 'react';
import { Provider } from 'react-redux';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { store } from './redux/store';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import ExpenseListPage from './components/ExpenseListPage';
import ExpenseFormPage from './components/ExpenseFormPage';
import Navigation from './components/Navigation';
import ProtectedRoute from './components/ProtectedRoute';
import './index.css';

function App() {
  return (
    <Provider store={store}>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />

          {/* Protected Routes Wrapper */}
          <Route path="/*" element={
            <ProtectedRoute>
              <div className="min-h-screen bg-gray-50 flex flex-col">
                <Navigation />
                <main className="flex-1 py-8 px-4 sm:px-6 lg:px-8">
                  <div className="max-w-7xl mx-auto">
                    <Routes>
                      <Route path="/dashboard" element={<Dashboard />} />
                      <Route path="/expenses" element={<ExpenseListPage />} />
                      <Route path="/add-expense" element={<ExpenseFormPage />} />
                      <Route path="*" element={<Navigate to="/dashboard" replace />} />
                    </Routes>
                  </div>
                </main>
              </div>
            </ProtectedRoute>
          } />
        </Routes>
      </Router>
    </Provider>
  );
}

export default App;