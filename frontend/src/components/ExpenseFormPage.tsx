import React from 'react';
import ExpenseForm from './ExpenseForm';

const ExpenseFormPage: React.FC = () => {
  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-xl shadow-sm p-8">
        <ExpenseForm />
      </div>
    </div>
  );
};

export default ExpenseFormPage;
