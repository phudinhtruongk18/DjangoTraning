"""
CRUD product:
    - SINGLE
    - LIST (create, read, delete)
- read is always available
- create when login
- edit when owner or admin
- delete when owner or admin
"""
from django.db import IntegrityError, transaction
# import count
from django.db.models import Count, F, Value

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from product.models import Product,Photo
from product.permissions import IsProcductOwnerOrReadOnly

from .serializers import ProductSerializer,PhotoSerializer
from .short_serializers import CreateProductSerializer,ListProductSerializer

from .serializers import ReportProductSerializer,CommentProductSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# -------------------- SINGLE --------------------


class CreatePhotoApiView(generics.CreateAPIView):
    """
    create a new photo
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = PhotoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # i want create a new photo if know user is owner
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

class PhotoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsProcductOwnerOrReadOnly]


# -------------------- SINGLE --------------------


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


# -------------------- LIST --------------------


class ProductCreateAPIView(generics.CreateAPIView):
    """ this view only hanlde product and it's exist category (not contain photos)"""
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    # def get_serializer(self, *args, **kwargs):
    #     # print("if 0")
    #     if "data" in kwargs:
    #         # print("if 1")
    #         data = kwargs["data"]

    #         if isinstance(data, list):
    #             kwargs["many"] = True
    #             # print("if 2")

    #     return super(ProductCreateAPIView, self).get_serializer(*args, **kwargs)


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer

# # optimize 4,6 sec to 349ms
# @api_view(['GET'])
# def get_report_product_list(request):
#     """
#     Return a list of products which has most views
#     """
#     products = Product.objects.values("name","hit_count_generic__hits")
#     serializer = ReportProductSerializer(products, many=True)
#     return Response(serializer.data)

# class view

class CommentProductListAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = CommentProductSerializer

# -------------------- LIST --------------------
