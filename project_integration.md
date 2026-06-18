# Integration & Post-Setup Guide

Once you have both the Django backend and the React frontend running, you must integrate them so data flows seamlessly. This document covers integration, common pitfalls, and testing.

## 1. API Connection (Redux Thunks)
Instead of updating local Redux state synchronously, you must use `createAsyncThunk` in your Redux slices to interact with Django.

Example of fetching expenses in `expenseSlice.ts`:
```typescript
export const fetchExpenses = createAsyncThunk('expenses/fetchExpenses', async () => {
  const response = await axios.get('http://localhost:8000/api/expenses/');
  
  // Note: Django REST Framework returns paginated data by default!
  // The actual array of data is inside `response.data.results`.
  const dataList = response.data.results ? response.data.results : response.data;
  
  return dataList;
});
```

> [!WARNING]
> **Pagination Trap:** A very common mistake is calling `.map()` directly on `response.data`. If DRF pagination is enabled, `response.data` is an object containing a `results` array, not an array itself!

## 2. Handling CSRF and CORS
When connecting a local React app (`localhost:3000`) to a local Django app (`localhost:8000`), you will face two common security blocks:

1. **CORS Error:** Fixed by adding `localhost:3000` to `CORS_ALLOWED_ORIGINS` in Django `settings.py` (covered in Backend Setup).
2. **CSRF Token Missing:** By default, Django enforces CSRF tokens on POST/DELETE requests. For a simple local setup/demo, disabling `SessionAuthentication` in `REST_FRAMEWORK` settings prevents Django from blocking local API requests. For a production app, you would need to fetch the CSRF token via Axios or implement JWT/Token-based authentication.

## 3. Simultaneous Execution
You must run two separate terminal windows simultaneously:
- **Terminal 1 (Backend):** `python manage.py runserver` (Runs on Port 8000)
- **Terminal 2 (Frontend):** `npm start` (Runs on Port 3000)

## 4. Testing End-to-End Flow
To verify your project is fully connected:
1. Open the React app at `localhost:3000`.
2. Navigate to the **Add Expense** page.
3. Fill out the form and submit.
4. Go to your Django Admin (`localhost:8000/admin/`) and verify the row was physically created in the database.
5. Go to the **Dashboard** page in React and verify the Donut Chart immediately reflects the newly added database record.

## 5. Next Steps for Production Deployment
When you are ready to take this project live on the internet:
- **Database**: Switch from SQLite to **PostgreSQL**.
- **Backend Hosting**: Deploy the Django API to **Render**, **Heroku**, or **DigitalOcean**.
- **Frontend Hosting**: Deploy the compiled React build to **Vercel** or **Netlify**.
- **Environment Variables**: Move hardcoded URLs like `http://localhost:8000` into `.env` files (e.g., `REACT_APP_API_URL`).
