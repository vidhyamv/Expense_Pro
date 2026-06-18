from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Sum
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer, ExpenseStatsSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user, _ = User.objects.get_or_create(username='demo', defaults={'email': 'demo@example.com'})
        return Expense.objects.filter(user=user)
    
    def perform_create(self, serializer):
        user, _ = User.objects.get_or_create(username='demo', defaults={'email': 'demo@example.com'})
        serializer.save(user=user)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get expense statistics"""
        expenses = self.get_queryset()
        
        total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        
        by_category = {}
        for category in Category.objects.all():
            category_total = expenses.filter(category=category).aggregate(Sum('amount'))['amount__sum'] or 0
            if category_total > 0:
                by_category[category.name] = float(category_total)
        
        # Monthly trend
        last_6_months = []
        for i in range(6):
            month_start = datetime.now() - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            month_total = expenses.filter(
                date__gte=month_start,
                date__lt=month_end
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            
            last_6_months.insert(0, {
                'month': month_start.strftime('%B'),
                'amount': float(month_total)
            })
        
        data = {
            'total': float(total),
            'by_category': by_category,
            'monthly_trend': last_6_months,
        }
        
        serializer = ExpenseStatsSerializer(data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get expenses filtered by category"""
        category_id = request.query_params.get('category_id')
        if category_id:
            expenses = self.get_queryset().filter(category_id=category_id)
        else:
            expenses = self.get_queryset()
        
        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def date_range(self, request):
        """Get expenses within a date range"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        expenses = self.get_queryset()
        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        if end_date:
            expenses = expenses.filter(date__lte=end_date)
        
        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]