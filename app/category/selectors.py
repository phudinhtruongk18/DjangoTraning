from django.db.models.query import QuerySet
from django.db.models import Count

from .models import Category
from user.models import NomalUser

def get_rp_categories() -> QuerySet[Category]:
    return Category.objects.annotate(num_products=Count('product')).order_by('-num_products')
