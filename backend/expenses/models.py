from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Expense category model."""

    ICON_CHOICES = [
        ('food', 'Food & Dining'),
        ('transport', 'Transport'),
        ('shopping', 'Shopping'),
        ('entertainment', 'Entertainment'),
        ('health', 'Health & Medical'),
        ('education', 'Education'),
        ('utilities', 'Utilities'),
        ('rent', 'Rent & Housing'),
        ('salary', 'Salary'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True,
        blank=True,
        help_text='Null means system-level default category'
    )
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='other')
    color = models.CharField(max_length=7, default='#6C757D', help_text='Hex color code e.g. #FF5733')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name


class Expense(models.Model):
    """Expense transaction model."""

    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Credit / Debit Card'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    receipt_image = models.ImageField(upload_to='receipts/', null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, default='', help_text='Comma-separated tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - ₹{self.amount} ({self.date})"
