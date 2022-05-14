from django.core.exceptions import ValidationError

def validate_owner(value):
    if not value:
        raise ValidationError("Owner is required")
    return value
    