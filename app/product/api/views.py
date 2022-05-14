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

from product.models import Product,Photo
from product.my_permissions import IsProductOwnerOrReadOnly

from .serializers import ProductSerializer,PhotoSerializer
from .short_serializers import ShortProductSerializer
from .serializers import ReportProductSerializer,CommentProductSerializer
from rest_framework.authtoken.models import Token


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsProductOwnerOrReadOnly]

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    lookup_field = 'pk'

# -------------------- SINGLE --------------------


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.DjangoObjectPermissions]
    authentication = (authentication.TokenAuthentication,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    # def get(self, request, *args, **kwargs):
    #     print(request.user.is_authenticated)
    #     return self.retrieve(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

# -------------------- LIST --------------------


class ProductListCreateAPIView(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ShortProductSerializer

    def perform_create(self, serializer):
        # get token
        user = Token.objects.get(key=self.request.POST['token']).user
        serializer.save(owner=user)
        return super().perform_create(serializer)


class ReportProductListAPIView(generics.ListAPIView):
    pagination_class = None
    queryset = Product.objects.all()
    serializer_class = ReportProductSerializer


class CommentProductListAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = CommentProductSerializer

