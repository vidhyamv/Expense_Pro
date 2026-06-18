//Represents a logged-in user.
export interface User {
    id: string;
    email: string;
    name: string;
}

//Represents a single expense.
export interface Expense {
    id: string;
    category: string;
    amount: number;
    description: string;
    date: string;
    userId: string;
}

// Additional common types for the application
export interface ExpenseFilter {
    category?: string;
    startDate?: string;
    endDate?: string;
    sortBy?: 'date' | 'amount';
    order?: 'asc' | 'desc';
}

//Represents the response received after login.
export interface AuthResponse {
    user: User;
    token: string;
}
//Used for reports and charts.
export interface ExpenseStats {
    totalAmount: number;
    categoryBreakdown: Record<string, number>;
    monthlyAverage?: number;
}
