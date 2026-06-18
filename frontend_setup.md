# Frontend Setup Guide (React & Redux)

This document outlines the steps to recreate the React frontend for the **Expense Tracker Pro** project from scratch.

## 1. Prerequisites
- Node.js (v18+)
- npm or yarn

## 2. Initialize the React App
We will use Create React App with the TypeScript template for type safety.
```bash
npx create-react-app frontend --template typescript
cd frontend
```

## 3. Install Dependencies
Install the required packages for routing, state management, API requests, and charting:
```bash
npm install react-router-dom axios recharts
npm install @reduxjs/toolkit react-redux
```

## 4. Install & Configure Tailwind CSS
Tailwind is used for the modern, professional UI.
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```
Update your `tailwind.config.js`:
```javascript
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```
Add Tailwind directives to the top of `src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## 5. Set Up Redux Toolkit
1. **Create Slices:** Create `src/redux/expenseSlice.ts` to manage your expense state array.
2. **Configure Store:** Create `src/redux/store.ts` using `configureStore` and combine your slices.
3. **Provide Store:** In `src/index.tsx`, wrap your `<App />` component in the Redux `<Provider store={store}>`.

## 6. Build the Component Architecture
Organize your components logically in the `src/components/` folder:
- **`Navigation.tsx`**: Top-level Navbar using `react-router-dom`'s `<Link>` tags.
- **`Dashboard.tsx`**: High-level statistical view showing total amounts and the pie chart.
- **`ExpenseChart.tsx`**: A Donut chart built using Recharts `PieChart` and `Cell`.
- **`ExpenseListPage.tsx`**: A full-screen page rendering the table of all expenses.
- **`ExpenseFormPage.tsx`**: The form inputs to add a new expense.

## 7. Configure React Router
In `src/App.tsx`, set up the main layout and routing. Example:
```tsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Navigation />
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/expenses" element={<ExpenseListPage />} />
        <Route path="/add-expense" element={<ExpenseFormPage />} />
      </Routes>
    </Router>
  );
}
```

## 8. Run the Application
```bash
npm start
```
Your frontend will start on `http://localhost:3000/`.
