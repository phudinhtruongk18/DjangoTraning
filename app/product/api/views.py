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

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

from product.models import Product,Photo
from product.permissions import IsPhotoOwnerOrReadOnly

from .serializers import ProductSerializer,PhotoSerializer
from .short_serializers import CreateProductSerializer,ListProductSerializer

from .serializers import ReportProductSerializer,CommentProductSerializer

# -------------------- SINGLE --------------------


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPhotoOwnerOrReadOnly]

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    lookup_field = 'pk'


# -------------------- SINGLE --------------------


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer
    authentication_classes = (TokenAuthentication,)


class ReportProductListAPIView(generics.ListAPIView):
    pagination_class = None
    queryset = Product.objects.all()
    serializer_class = ReportProductSerializer


class CommentProductListAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = CommentProductSerializer

# -------------------- LIST --------------------
