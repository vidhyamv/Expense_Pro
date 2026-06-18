import { configureStore } from '@reduxjs/toolkit';
import expenseReducer from './expenseSlice';
import authReducer from './authSlice';

export const store = configureStore({
    reducer: {
        expenses: expenseReducer,
        auth: authReducer,
    },
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
