from rest_framework import viewsets

from category.models import Category
from .serializers import DetailCategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = DetailCategorySerializer
