from django.core.exceptions import ValidationError
from .models import Category
from rest_framework.validators import UniqueValidator

def validate_owner(value):
    if not value:
        raise ValidationError("Owner is required")
    return value

def validate_name(value):
    exist = Category.objects.filter(name__iexact=value).exists()
    if exist:
        raise ValidationError("Category already exists")
    return value

unique_validator = UniqueValidator(queryset=Category.objects.all(), message="Category already exists 2")