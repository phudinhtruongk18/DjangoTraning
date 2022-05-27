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
from .serializers import DetailCategorySerializer,CategorySerializer
from .serializers import ReportCategorySerializer
# import permision IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# -------------------- SINGLE --------------------

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication = (TokenAuthentication,)
    queryset = Category.objects.all()
    serializer_class = DetailCategorySerializer
    lookup_field = 'pk'

# -------------------- LIST --------------------


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
# simple function view to get all categories and its num of product
@api_view(['GET'])
def products_quantity_per_category(request):
    categories = Category.objects.annotate(num_products=Count('product')).order_by('-num_products')
    serializer = ReportCategorySerializer(categories, many=True,context={'request': request})
    return Response(serializer.data)
    