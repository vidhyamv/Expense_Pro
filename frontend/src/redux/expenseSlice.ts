import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { Expense } from '../types/types';

interface ExpenseState {
  expenses: Expense[];
  loading: boolean;
  error: string | null;
}

const initialState: ExpenseState = {
  expenses: [],
  loading: false,
  error: null,
};

// Safely determine API URL based on where the frontend is running
const isProduction = typeof window !== 'undefined' && window.location.hostname !== 'localhost';
const API_URL = isProduction 
  ? 'https://expense-pro-backend.onrender.com/api/expenses/' 
  : 'http://localhost:8000/api/expenses/';

// Fetch expenses from backend
export const fetchExpenses = createAsyncThunk('expenses/fetchExpenses', async () => {
  const response = await axios.get(API_URL);

  // Handle paginated response ({count, results: []}) or direct array
  const dataList = response.data.results ? response.data.results : response.data;

  return dataList.map((item: any) => ({
    id: item.id.toString(),
    category: item.category_detail ? item.category_detail.name : 'Other',
    amount: parseFloat(item.amount),
    description: item.title, // Backend uses title, frontend uses description
    date: item.date,
    userId: item.user?.toString() || 'guest',
  }));
});

// Add new expense
export const addExpenseThunk = createAsyncThunk('expenses/addExpense', async (expense: Omit<Expense, 'id'>) => {
  const payload = {
    category_name: expense.category, // using the write-only field we added to serializer
    amount: expense.amount,
    title: expense.description, // frontend description maps to backend title
    date: expense.date,
  };
  const response = await axios.post(API_URL, payload);
  const item = response.data;
  return {
    id: item.id.toString(),
    category: item.category_detail ? item.category_detail.name : expense.category,
    amount: parseFloat(item.amount),
    description: item.title,
    date: item.date,
    userId: item.user?.toString() || 'guest',
  };
});

// Delete expense
export const deleteExpenseThunk = createAsyncThunk('expenses/deleteExpense', async (id: string) => {
  await axios.delete(`${API_URL}${id}/`);
  return id;
});

const expenseSlice = createSlice({
  name: 'expenses',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    // Fetch
    builder.addCase(fetchExpenses.pending, (state) => {
      state.loading = true;
    });
    builder.addCase(fetchExpenses.fulfilled, (state, action) => {
      state.loading = false;
      state.expenses = action.payload;
    });
    builder.addCase(fetchExpenses.rejected, (state, action) => {
      state.loading = false;
      state.error = action.error.message || 'Failed to fetch expenses';
    });

    // Add
    builder.addCase(addExpenseThunk.fulfilled, (state, action) => {
      state.expenses.push(action.payload);
    });

    // Delete
    builder.addCase(deleteExpenseThunk.fulfilled, (state, action) => {
      state.expenses = state.expenses.filter(exp => exp.id !== action.payload);
    });
  },
});

export default expenseSlice.reducer;
