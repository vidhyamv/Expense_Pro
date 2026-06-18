import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';
import ExpenseChart from './ExpenseChart';
import { fetchExpenses } from '../redux/expenseSlice';
import '../styles/Dashboard.scss'; 

const Dashboard: React.FC = () => {
  const dispatch = useDispatch<any>();
  const expenses = useSelector((state: RootState) => state.expenses.expenses);
  const [stats, setStats] = useState({
    total: 0,
    byCategory: {} as { [key: string]: number },
  });

  useEffect(() => {
    dispatch(fetchExpenses());
  }, [dispatch]);

  useEffect(() => {
    const total = expenses.reduce((sum, exp) => sum + exp.amount, 0);
    const byCategory: { [key: string]: number } = {};
    
    expenses.forEach(exp => {
      byCategory[exp.category] = (byCategory[exp.category] || 0) + exp.amount;
    });

    setStats({ total, byCategory });
  }, [expenses]);

  return (
    <div className="space-y-6">
      {/* Dashboard Header / Stats */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Overview</h1>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="bg-blue-50 rounded-xl p-5 border border-blue-100">
            <h3 className="text-sm font-medium text-blue-600 mb-1">Total Expenses</h3>
            <p className="text-4xl font-bold text-gray-900">₹{stats.total.toFixed(2)}</p>
          </div>
          <div className="bg-purple-50 rounded-xl p-5 border border-purple-100">
            <h3 className="text-sm font-medium text-purple-600 mb-1">Categories Used</h3>
            <p className="text-4xl font-bold text-gray-900">{Object.keys(stats.byCategory).length}</p>
          </div>
          <div className="bg-green-50 rounded-xl p-5 border border-green-100">
            <h3 className="text-sm font-medium text-green-600 mb-1">Transactions</h3>
            <p className="text-4xl font-bold text-gray-900">{expenses.length}</p>
          </div>
        </div>
      </div>

      {/* Chart */}
      <div className="bg-white rounded-xl shadow-sm p-6">
          <ExpenseChart categoryStats={stats.byCategory} />
      </div>
    </div>
  );
};

export default Dashboard;
