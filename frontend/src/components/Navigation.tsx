import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../redux/authSlice';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { RootState } from '../redux/store';

const Navigation: React.FC = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const user = useSelector((state: RootState) => state.auth.user);
  const isAuthenticated = useSelector(
    (state: RootState) => state.auth.isAuthenticated
  );

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  if (!isAuthenticated) {
    return null;
  }

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="bg-white shadow-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          
          {/* Logo & Links */}
          <div className="flex items-center space-x-8">
            <Link to="/dashboard" className="flex items-center">
              <h1 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 tracking-tight hover:opacity-80 transition-opacity">
                Expense Pro
              </h1>
            </Link>
            
            <div className="hidden md:flex space-x-4">
              <Link 
                to="/dashboard" 
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/dashboard') ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}`}
              >
                Dashboard
              </Link>
              <Link 
                to="/expenses" 
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/expenses') ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}`}
              >
                All Expenses
              </Link>
              <Link 
                to="/add-expense" 
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${isActive('/add-expense') ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}`}
              >
                Add New
              </Link>
            </div>
          </div>

          {/* User Info & Logout */}
          <div className="flex items-center space-x-6">
            <div className="hidden sm:block text-sm text-gray-600">
              Welcome, <span className="font-semibold text-gray-900">{user?.name}</span>
            </div>
            <button
              onClick={handleLogout}
              className="text-gray-500 hover:text-red-600 font-medium text-sm transition-colors flex items-center"
            >
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;