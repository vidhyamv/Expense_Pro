from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Expense


# ──────────────────────────────────────────────
# User Serializer
# ──────────────────────────────────────────────

class UserSerializer(serializers.ModelSerializer):
    """Read-only serializer for basic user info."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, label='Confirm Password')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
        )
        return user


# ──────────────────────────────────────────────
# Category Serializer
# ──────────────────────────────────────────────

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for expense categories."""

    expense_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'icon', 'color',
            'is_default', 'expense_count', 'created_at'
        ]
        read_only_fields = ['id', 'is_default', 'created_at', 'expense_count']

    def get_expense_count(self, obj):
        return obj.expenses.count()

    def create(self, validated_data):
        return super().create(validated_data)


# ──────────────────────────────────────────────
# Expense Serializer
# ──────────────────────────────────────────────

class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for expense transactions."""

    # Nested read — shows full category details on GET
    category_detail = CategorySerializer(source='category', read_only=True)

    # Write — accepts category ID on POST/PUT
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True,
        required=False
    )
    
    # Optional field to accept category by name
    category_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Expense
        fields = [
            'id', 'user', 'category', 'category_detail', 'category_name',
            'title', 'description', 'amount', 'date',
            'payment_method', 'receipt_image', 'tags',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'user', 'category_detail', 'created_at', 'updated_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than zero.')
        return value

    def create(self, validated_data):
        category_name = validated_data.pop('category_name', None)
        if category_name:
            cat, _ = Category.objects.get_or_create(name=category_name)
            validated_data['category'] = cat
        return super().create(validated_data)


class ExpenseSummarySerializer(serializers.Serializer):
    """Read-only serializer for aggregated expense summary."""

    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_count = serializers.IntegerField()
    by_category = serializers.ListField(child=serializers.DictField())
    by_payment_method = serializers.ListField(child=serializers.DictField())

class ExpenseStatsSerializer(serializers.Serializer):
    """Read-only serializer for expense statistics."""
    total = serializers.FloatField()
    by_category = serializers.DictField(child=serializers.FloatField())
    monthly_trend = serializers.ListField(child=serializers.DictField())
