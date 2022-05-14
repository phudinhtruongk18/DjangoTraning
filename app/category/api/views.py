"""
CRUD category:
    - SINGLE
    - LIST (create, read, delete)
- read is always available
- create when login
- edit when owner or admin
- delete when owner or admin
"""
from category.models import Category
from .serializers import CategorySerializer,ShortCategorySerializer
from rest_framework import generics

from rest_framework import permissions
from rest_framework import authentication

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from .serializers import ReportCategorySerializer

# -------------------- SINGLE --------------------

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.DjangoObjectPermissions]
    authentication = (authentication.TokenAuthentication,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

    # def get(self, request, *args, **kwargs):
    #     print(request.user.is_authenticated)
    #     return self.retrieve(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

# -------------------- LIST --------------------

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied

from rest_framework.authentication import TokenAuthentication

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = ShortCategorySerializer
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        # get token

        user = Token.objects.get(key=self.request.POST['token']).user
        # if anonymous user, return error

        # print(self.request.user)
        # user = self.request.user

        if user.is_anonymous:
            raise PermissionDenied("No permission to create category")

        serializer.save(owner=user)
        return super().perform_create(serializer)

# simple function view to get all categories and its num of product
@api_view(['GET'])
def products_quantity_per_category(request):
    categories = Category.objects.annotate(num_products=Count('product')).order_by('-num_products')
    serializer = ReportCategorySerializer(categories, many=True,context={'request': request})
    return Response(serializer.data)
    