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
from .serializers import CategorySerializer
from rest_framework import generics

from rest_framework import permissions
from rest_framework import authentication


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

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        # get token
        user = Token.objects.get(key=self.request.POST['token']).user
        serializer.save(owner=user)
        return super().perform_create(serializer)
