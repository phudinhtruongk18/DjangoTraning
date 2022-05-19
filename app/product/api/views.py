"""
CRUD product:
    - SINGLE
    - LIST (create, read, delete)
- read is always available
- create when login
- edit when owner or admin
- delete when owner or admin
"""
from rest_framework import generics
from rest_framework import authentication

from product.models import Product,Photo,Category
from product.my_permissions import IsProductOwnerOrReadOnly

from .serializers import ProductSerializer,PhotoSerializer
from .short_serializers import ShortProductSerializer
from .serializers import ReportProductSerializer,CommentProductSerializer
from rest_framework.authtoken.models import Token

from rest_framework.validators import ValidationError
from rest_framework.exceptions import PermissionDenied

from django.db import IntegrityError, transaction

class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsProductOwnerOrReadOnly]

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    lookup_field = 'pk'

# -------------------- SINGLE --------------------

from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.DjangoObjectPermissions]
    # authentication = (authentication.TokenAuthentication,)
    authentication_classes = [TokenAuthentication]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    # def get(self, request, *args, **kwargs):
    #     print(request.user.is_authenticated)
    #     return self.retrieve(request, *args, **kwargs)

    # def get_queryset(self):
    #     print(self.request.user)
    #     return super().get_queryset()

    # def delete(self, request, *args, **kwargs):
    #     product = self.get_object()
    #     if product.owner != request.user:
    #         raise PermissionDenied("You are not the owner of this product")
        
    #     return self.destroy(request, *args, **kwargs)
    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

# -------------------- LIST --------------------

from rest_framework.authentication import TokenAuthentication

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ShortProductSerializer
    authentication_classes = (TokenAuthentication,)
    
    def perform_create(self, serializer):
        # get token
        # print(self.request.POST,"<-")
        user = self.request.user
        
        if user.is_anonymous:
            raise PermissionDenied({"token":"No permission to create category"})

        categories_of_product = []
        categories = self.request.POST.getlist('categories')
        # print('->',categories)
        for category in categories:
            # print(category)
            try:
                pk_pro = int(category)
                # print("->",pk_pro)
                category_obj = Category.objects.get(pk=pk_pro)
                categories_of_product.append(category_obj)
            except Category.DoesNotExist:
                # pass
                raise ValidationError({'categories': 'Category with pk:'+str(category)+' does not exist'})

        with transaction.atomic():
            product = serializer.save(owner=user,categories=categories_of_product)
            # serializer.save(owner=user,categories=categories_of_product)
            # print(serializer)
            # categories_of_product = Category.objects.get(pk=3)

            # instance
            try:
                for photo in self.request.FILES.getlist('photos'):
                    Photo.objects.create(image=photo,product=product)
            except Exception as e:
                print("IntegrityError", e)
                raise ValidationError({'photos': 'Some photos are not uploaded'})
                
            serializer.save()

        # return super().perform_create(serializer)


class ReportProductListAPIView(generics.ListAPIView):
    pagination_class = None
    queryset = Product.objects.all()
    serializer_class = ReportProductSerializer


class CommentProductListAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = CommentProductSerializer

