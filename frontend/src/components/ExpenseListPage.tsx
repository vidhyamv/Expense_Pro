import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';
import ExpenseList from './ExpenseList';
import { fetchExpenses } from '../redux/expenseSlice';

const ExpenseListPage: React.FC = () => {
  const dispatch = useDispatch<any>();
  const expenses = useSelector((state: RootState) => state.expenses.expenses);

  useEffect(() => {
    dispatch(fetchExpenses());
  }, [dispatch]);

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <ExpenseList expenses={expenses} />
    </div>
  );
};

export default ExpenseListPage;
