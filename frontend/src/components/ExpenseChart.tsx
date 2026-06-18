import React from 'react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend
} from 'recharts';

interface ExpenseChartProps {
  categoryStats: Record<string, number>;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#FF6666', '#82CA9D'];

const ExpenseChart: React.FC<ExpenseChartProps> = ({ categoryStats }) => {
  // Transform the Record<string, number> into the array format Recharts expects
  const data = Object.entries(categoryStats).map(([name, value]) => ({
    name,
    value,
  }));

  if (data.length === 0) {
    return (
      <div className="expense-chart" style={{ textAlign: 'center', padding: '2rem 0' }}>
        <h3>Expenses by Category</h3>
        <p>No expenses yet. Add an expense to see the chart!</p>
      </div>
    );
  }

  return (
    <div className="expense-chart">
      <h3>Expenses by Category</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, value }) => `${name}: ₹${value}`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value: any) => `₹${Number(value).toFixed(2)}`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ExpenseChart;
