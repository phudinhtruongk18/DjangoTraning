from django.core.exceptions import ValidationError
from .models import Product
from rest_framework.validators import UniqueValidator

def validate_owner(value):
    if not value:
        raise ValidationError("Owner is required")
    return value

def validate_name(value):
    exist = Product.objects.filter(name__iexact=value).exists()
    if exist:
        raise ValidationError("Product already exists")
    return value

unique_validator = UniqueValidator(
    queryset=Product.objects.all(), 
    message="Product already exists 2",
    lookup='iexact'
    )