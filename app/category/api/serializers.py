from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.response import Response

from django.db.models import Count, F, Value

from category.validators import validate_name,validate_owner,unique_validator
from category.models import Category

from product.api.short_serializers import CreateProductSerializer


class CategoryListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.annotate(num_products=Count('product'))
        return super().to_representation(data)
    
    def create(self, validated_data):
        categories = [Category(**item) for item in validated_data]
        return Category.objects.bulk_create(categories)


class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('_owner',validators=[validate_owner],read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='category:my_category', lookup_field='pk',read_only=True)
    name = serializers.CharField(required=True, validators=[unique_validator])
    date_added = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    views_count = serializers.SerializerMethodField(read_only=True)

    image = serializers.ImageField(required=False)
    parent = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=Category.objects.all()
        )

    class Meta:
        model = Category
        fields = ('owner','url', 'name','date_added','image','views_count','parent')
        list_serializer_class = CategoryListSerializer
        

    def get_views_count(self, obj):
        return obj.hit_count.hits
    
    def _owner(self, obj):
        if obj.owner:
            return obj.owner.full_name()
        return None


class ReportCategorySerializer(CategorySerializer):
    "Report Category With num of book Serializer"
    num_products = serializers.SerializerMethodField()

    def get_num_products(self, obj):
        try:
            return obj.num_products
        except Exception:
            return None
            
    class Meta:
        model = Category
        fields = ('name', 'views_count', 'num_products')

