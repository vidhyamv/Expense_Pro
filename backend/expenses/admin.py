from django.contrib import admin
from .models import Expense, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_default')
    list_filter = ('is_default',)
    search_fields = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'date', 'user')
    list_filter = ('date', 'payment_method', 'category')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'
    ordering = ('-date',)
