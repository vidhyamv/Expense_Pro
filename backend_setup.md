# Backend Setup Guide — Django & Django REST Framework
## Expense Tracker Pro

This document gives you a **complete, step-by-step explanation** of how the Django backend for the Expense Tracker Pro was built from scratch. Every decision is explained so you can replicate it confidently.

---

## What the Backend Does

The backend is a **REST API** (Application Programming Interface) built with **Django** and **Django REST Framework (DRF)**. It:
- Stores all expense data in a database (SQLite for development).
- Exposes URL endpoints that the React frontend can call to fetch, create, and delete expenses.
- Provides a built-in Admin panel at `/admin/` so you can manage data through a visual interface.

---

## Prerequisites

Before starting, make sure the following are installed on your computer:
- **Python 3.10 or higher** — the programming language the backend is written in.
- **pip** — Python's package manager (comes pre-installed with Python).
- **A terminal** — Command Prompt, PowerShell, or any shell.

---

## Step 1: Create a Project Folder and Virtual Environment

A **virtual environment** is an isolated space for your Python packages. This prevents conflicts between different projects on the same computer.

```bash
# Navigate to your project folder (or create one)
mkdir expense-tracker-pro
cd expense-tracker-pro

# Create a virtual environment named "venv"
python -m venv venv

# Activate it on Windows
.\venv\Scripts\activate

# Activate it on Mac or Linux
source venv/bin/activate
```

After activation, your terminal prompt will show `(venv)` at the start, confirming the environment is active.

---

## Step 2: Install Required Packages

```bash
pip install django djangorestframework django-cors-headers
```

Here is what each package does:
- **`django`** — The main web framework. It handles URL routing, database interaction, admin panel, and more.
- **`djangorestframework`** — An extension on top of Django that makes building REST APIs easy. It provides Serializers, Viewsets, and Routers.
- **`django-cors-headers`** — A middleware that adds CORS (Cross-Origin Resource Sharing) headers to responses, which allows the React app running on port 3000 to make requests to Django on port 8000. Without this, the browser would block the communication.

---

## Step 3: Create the Django Project and App

In Django, a **project** is the top-level configuration for the entire site. An **app** is a module within the project that handles a specific feature.

```bash
# Create the project with a "config" folder to hold all settings
django-admin startproject config .

# The dot (.) at the end means create the project in the current directory.

# Create the "expenses" app
python manage.py startapp expenses
```

After this, you will have:
```
expense-tracker-pro/
├── config/          ← Project configuration (settings, main URLs)
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── expenses/        ← Our app (models, views, serializers)
│   ├── models.py
│   ├── views.py
│   └── ...
└── manage.py        ← Django's command-line tool
```

---

## Step 4: Configure `settings.py`

Open `config/settings.py`. This file controls everything about the Django project.

### 4a. Add Your Apps to `INSTALLED_APPS`

Django needs to know which apps are part of the project. Find the `INSTALLED_APPS` list and add:

```python
INSTALLED_APPS = [
    'django.contrib.admin',       # Admin panel (built-in)
    'django.contrib.auth',        # User authentication (built-in)
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # --- Third-party packages ---
    'rest_framework',             # Django REST Framework
    'corsheaders',                # CORS handling for React frontend
    # --- Your custom app ---
    'expenses',
]
```

### 4b. Add CORS Middleware

Find the `MIDDLEWARE` list and add `'corsheaders.middleware.CorsMiddleware'` as the **very first item** in the list. It must be first so it can process requests before anything else:

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← ADD THIS FIRST
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ... rest of the default middleware
]
```

### 4c. Configure DRF and CORS at the Bottom of the File

Add these settings at the very bottom of `settings.py`:

```python
# Tell CORS which frontend domains are allowed to make requests
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',   # React development server
    'http://localhost:8000',
]

# Configure Django REST Framework behavior
REST_FRAMEWORK = {
    # Empty list disables CSRF enforcement for simple local development/testing.
    # For a production app, you would use JWT or Token Authentication here.
    'DEFAULT_AUTHENTICATION_CLASSES': [],

    # Automatically splits large lists of data into pages of 10 items.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

---

## Step 5: Define the Database Models (`models.py`)

A **Model** is a Python class that represents a database table. Each attribute on the class becomes a column in the table.

Open `expenses/models.py` and define the two models:

```python
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Expense category (e.g., Food, Transport, Health)."""

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

    # ForeignKey links this Category to a User. null=True means a Category
    # can also be a "system-level" category with no specific owner.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='categories', null=True, blank=True,
        help_text='Null means system-level default category'
    )
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='other')
    color = models.CharField(max_length=7, default='#6C757D', help_text='Hex color e.g. #FF5733')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) # Set automatically when created

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']             # Always sorted alphabetically by name
        unique_together = ('user', 'name')  # Same user can't have two categories with the same name

    def __str__(self):
        return self.name  # Shows the name in Admin panel


class Expense(models.Model):
    """A single expense transaction."""

    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Credit / Debit Card'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    
    # SET_NULL means if the category is deleted, the expense is kept but
    # its category is set to null, not deleted.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    
    # MinValueValidator ensures that you cannot enter 0 or a negative amount.
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    
    date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    receipt_image = models.ImageField(upload_to='receipts/', null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, default='', help_text='Comma-separated tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Updated every time the record is saved

    class Meta:
        ordering = ['-date', '-created_at']  # Newest expenses appear first

    def __str__(self):
        return f"{self.title} - ₹{self.amount} ({self.date})"
```

---

## Step 6: Create Serializers (`serializers.py`)

A **Serializer** converts complex Python objects (like database model instances) into simple Python dictionaries, which can then be turned into JSON for the API response. It also works in reverse — it validates incoming JSON and converts it back into a model instance to save.

Create `expenses/serializers.py`:

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    """Converts Category objects to/from JSON."""

    # SerializerMethodField lets you add a calculated field that isn't a real
    # database column — in this case, the count of expenses in a category.
    expense_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'color', 'is_default', 'expense_count', 'created_at']
        read_only_fields = ['id', 'is_default', 'created_at', 'expense_count']

    def get_expense_count(self, obj):
        # `obj` is the Category instance. This counts its related expenses.
        return obj.expenses.count()


class ExpenseSerializer(serializers.ModelSerializer):
    """Converts Expense objects to/from JSON."""

    # On GET requests, this will include full category details (name, color, etc.)
    # as a nested object. `source='category'` tells DRF to read from the category field.
    category_detail = CategorySerializer(source='category', read_only=True)

    # On POST requests, the frontend can send a category ID (integer) to link an expense.
    # This field accepts the ID for writing.
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True, required=False
    )

    # This is a special write-only field: the frontend can POST the category name
    # as a plain string (e.g., "Food") instead of an ID. The `create()` method
    # handles looking up or creating the category by name.
    category_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Expense
        fields = [
            'id', 'user', 'category', 'category_detail', 'category_name',
            'title', 'description', 'amount', 'date',
            'payment_method', 'receipt_image', 'tags', 'created_at', 'updated_at',
        ]
        # `user` and `category_detail` are always read-only — the API sets them automatically.
        read_only_fields = ['id', 'user', 'category_detail', 'created_at', 'updated_at']

    def validate_amount(self, value):
        # Custom validator: runs when the serializer checks the `amount` field.
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than zero.')
        return value

    def create(self, validated_data):
        # This overrides the default create logic to handle category_name.
        # `pop` removes 'category_name' from the dict so it isn't passed to
        # the Expense model directly (the model doesn't have that field).
        category_name = validated_data.pop('category_name', None)
        if category_name:
            # get_or_create: looks for a category with this name.
            # If it doesn't exist, it creates one. Returns (object, created_boolean).
            cat, _ = Category.objects.get_or_create(name=category_name)
            validated_data['category'] = cat
        return super().create(validated_data)
```

---

## Step 7: Create the API Views (`views.py`)

A **ViewSet** is a class that handles all API operations (list, create, retrieve, update, delete) for a model in one place. Using `ModelViewSet` gives you all of these automatically.

Open `expenses/views.py`:

```python
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer, ExpenseStatsSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    # AllowAny means no login is required — perfect for a demo.
    permission_classes = [AllowAny]

    def get_queryset(self):
        # All API calls will filter expenses for the "demo" user only.
        # get_or_create will create this user the first time it runs.
        user, _ = User.objects.get_or_create(username='demo', defaults={'email': 'demo@example.com'})
        return Expense.objects.filter(user=user)

    def perform_create(self, serializer):
        # When a new expense is saved, automatically link it to the "demo" user.
        user, _ = User.objects.get_or_create(username='demo', defaults={'email': 'demo@example.com'})
        serializer.save(user=user)
```

---

## Step 8: Set Up URL Routing (`urls.py`)

A **Router** automatically generates all the URL patterns for a ViewSet (`GET /expenses/`, `POST /expenses/`, `DELETE /expenses/1/`, etc.)

Create `expenses/urls.py`:
```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ExpenseViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', include(router.urls)),
]
```

Then, in `config/urls.py`, include the expenses URLs under the `/api/` prefix:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('expenses.urls')),  # All our API endpoints under /api/
]
```

---

## Step 9: Register Models with Django Admin (`admin.py`)

The **Django Admin** is a powerful, auto-generated web interface for managing database records. You just need to register your models to enable it.

Open `expenses/admin.py`:
```python
from django.contrib import admin
from .models import Expense, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_default')  # Columns visible in the list view
    list_filter = ('is_default',)                  # Filter sidebar on the right
    search_fields = ('name',)                      # Search bar at the top

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'date', 'user')
    list_filter = ('date', 'payment_method', 'category')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'   # Calendar drill-down navigation at the top
    ordering = ('-date',)     # Show newest first
```

---

## Step 10: Run Migrations and Start the Server

**Migrations** are Django's way of creating and updating database tables based on your model definitions.

```bash
# Step 1: Generate migration files from your models
python manage.py makemigrations

# Step 2: Apply those migration files to create the actual database tables
python manage.py migrate

# Step 3: Create an admin superuser account so you can access /admin/
python manage.py createsuperuser
# (Follow the prompts to set a username and password)

# Step 4: Start the development server
python manage.py runserver
```

Your backend API is now fully running! You can access:
- **API Root:** `http://localhost:8000/api/`
- **Expenses API:** `http://localhost:8000/api/expenses/`
- **Admin Panel:** `http://localhost:8000/admin/`
