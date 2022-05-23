"""
CRUD category:
    - SINGLE
    - LIST (create, read, delete)
- read is always available
- create when login
- edit when owner or admin
- delete when owner or admin
"""
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count

from rest_framework.authentication import TokenAuthentication

from category.models import Category
from .serializers import CategorySerializer,ShortCategorySerializer
from .serializers import ReportCategorySerializer

# -------------------- SINGLE --------------------

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication = (TokenAuthentication,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

# -------------------- LIST --------------------


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    queryset = Category.objects.all()
    serializer_class = ShortCategorySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
# simple function view to get all categories and its num of product
@api_view(['GET'])
def products_quantity_per_category(request):
    categories = Category.objects.annotate(num_products=Count('product')).order_by('-num_products')
    serializer = ReportCategorySerializer(categories, many=True,context={'request': request})
    return Response(serializer.data)
    