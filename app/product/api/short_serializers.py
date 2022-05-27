from rest_framework import serializers

from product.my_validators import validate_name, unique_validator
from product.models import Product

from category.models import Category


class CategoryHyperLinkSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category:my_category', lookup_field='pk',
                                                read_only=True, format='html')

    class Meta:
        model = Category
        fields = ['url', 'name']

from django.db import IntegrityError, transaction

class ProductListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        products = []
        print(validated_data)

        # with transaction.atomic():

        for item in validated_data:
            print(item)
            print(item['name'])
            print(item['categories'])
            print(item['owner'])

            sing_product = Product(name=item['name'],owner=item['owner'])
            # sing_product.save()
            products.append(sing_product)
        
        return Product.objects.bulk_create(products)
            # sing_product.categories.set(item['categories'])

            # products.append(sing_product)

        # return Product.objects.bulk_create(products)
        # return Product.objects.bulk_update(products,['categories'])

class CreateProductSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product_detail', lookup_field='pk')
    date_added = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    name = serializers.CharField(required=True, validators=[validate_name,unique_validator])
    views_count = serializers.SerializerMethodField(read_only=True)
    
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Category.objects.all()
        )

    # trong thuc te thi viec upload anh se duoc handle rieng
    # photos = TempPhotoSerializer(source='photo_set',many=True,read_only=True)

    class Meta:
        model = Product
        fields = ('owner','url','date_added', 'name', 'views_count', 'thumb','categories')
        list_serializer_class = ProductListSerializer
    
    def get_owner(self, obj):
        if obj.owner:
            return obj.owner.username
        return None

    def get_views_count(self, obj):
        return obj.hit_count.hits

class ListProductSerializer(CreateProductSerializer):
    categories = CategoryHyperLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('owner','url','date_added', 'name', 'views_count', 'thumb','categories')

