"""
CRUD category:
    - SINGLE
    - LIST (create, read, delete)
- read is always available
- create when login
- edit when owner or admin
- delete when owner or admin
"""
from rest_framework import serializers

from rest_framework import generics
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Count

from rest_framework.authentication import TokenAuthentication

from category.models import Category
from .serializers import CategorySerializer
from .serializers import ReportCategorySerializer
# import permision IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# -------------------- SINGLE --------------------

# update service layer 30/5/22
from category import services
from category import selectors

# import inline serializers
from common.utils import inline_serializer

class CategoryDetailApi(views.APIView):
    class OutputSerializer(serializers.Serializer):
        url = serializers.HyperlinkedIdentityField(view_name='category:my_category', lookup_field='pk',read_only=True)
        owner = serializers.CharField()
        parent = serializers.PrimaryKeyRelatedField(
            read_only=False,
            queryset=Category.objects.all()
            )
        slug = serializers.CharField()
        name = serializers.CharField()
        date_added = serializers.DateTimeField()
        image = serializers.ImageField()
        views_count = serializers.IntegerField()

        products = inline_serializer(many=True, fields={
            'url': serializers.HyperlinkedIdentityField(view_name='product_detail', lookup_field='pk'),
            'owner': serializers.CharField(),
            'name': serializers.CharField(),
            'views_count': serializers.IntegerField(),
        })

    def get(self, request, pk):
        category = services.get_category_by_id(pk)
        print(category)
        serializer = self.OutputSerializer(category, context={'request': request})
        return Response(serializer.data)

class CategoryUpdateDeleteDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication = (TokenAuthentication,)
    queryset = Category.objects.all()
    # serializer_class = Re
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        category = services.category_update(category=instance, data=serializer.validated_data)

        # get serilize va lay data

        return Response(, status=status.HTTP_200_OK)
        # return Response({'id':category.id}, status=status.HTTP_200_OK)


# -------------------- LIST --------------------


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        owner = request.user

        validated_data = serializer.validated_data
        category = services.create_category(owner=owner,**validated_data)

        return Response({'id':category.id}, status=status.HTTP_201_CREATED)

        
class ProductQuantityPerCategory(views.APIView):
    class ReportCategorySerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)
        num_products = serializers.IntegerField()

    def get(self, request):
        categories = selectors.get_rp_categories()
        serializer = self.ReportCategorySerializer(categories, many=True)
        return Response(serializer.data)
