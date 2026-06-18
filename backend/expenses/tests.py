from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Category, Expense
from datetime import datetime, date, timedelta

class ExpenseTrackerTests(APITestCase):
    
    def setUp(self):
        # Create user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        # Create a category
        self.category = Category.objects.create(
            name='Food',
            user=self.user,
            icon='food'
        )
        
        # Create some expenses
        self.expense1 = Expense.objects.create(
            user=self.user,
            category=self.category,
            title='Lunch',
            amount=15.50,
            date=date.today()
        )
        self.expense2 = Expense.objects.create(
            user=self.user,
            category=self.category,
            title='Dinner',
            amount=25.00,
            date=date.today() - timedelta(days=1)
        )

    def test_category_list(self):
        """Test getting list of categories"""
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Food')

    def test_category_create(self):
        """Test creating a new category"""
        url = reverse('category-list')
        data = {
            'name': 'Transport',
            'icon': 'transport',
            'color': '#FF0000'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_expense_list(self):
        """Test getting list of expenses"""
        url = reverse('expense-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_expense_create(self):
        """Test creating a new expense"""
        url = reverse('expense-list')
        data = {
            'title': 'Coffee',
            'amount': 4.50,
            'date': date.today().strftime('%Y-%m-%d'),
            'category': self.category.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 3)

    def test_expense_stats(self):
        """Test the stats endpoint"""
        url = reverse('expense-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check total
        self.assertEqual(response.data['total'], 40.50) # 15.50 + 25.00
        # Check by_category
        self.assertIn('Food', response.data['by_category'])
        self.assertEqual(response.data['by_category']['Food'], 40.50)

    def test_expense_by_category(self):
        """Test filtering expenses by category endpoint"""
        url = reverse('expense-by-category')
        response = self.client.get(f'{url}?category_id={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_expense_date_range(self):
        """Test filtering expenses by date range endpoint"""
        url = reverse('expense-date-range')
        today_str = date.today().strftime('%Y-%m-%d')
        response = self.client.get(f'{url}?start_date={today_str}&end_date={today_str}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return today's expense (Lunch)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Lunch')

    def test_unauthenticated_access(self):
        """Test that API requires authentication"""
        self.client.logout()
        self.client.force_authenticate(user=None)
        
        url = reverse('expense-list')
        response = self.client.get(url)
        # Should return 401 or 403
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
