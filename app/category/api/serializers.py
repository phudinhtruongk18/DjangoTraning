from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.response import Response

from django.db.models import Count, F, Value

from category.my_validators import validate_name,validate_owner,unique_validator
from category.models import Category

from product.api.short_serializers import ShortProductSerializer

class ShortCategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category:test_api_sing', lookup_field='pk')
    name = serializers.CharField(required=True, validators=[validate_name,unique_validator])
    date_added = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    views_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ('url', 'name','date_added','image','views_count')

    def get_views_count(self, obj):
        return obj.hit_count.hits


class CategorySerializer(ShortCategorySerializer):
    owner = serializers.SerializerMethodField('_owner',validators=[validate_owner],read_only=True)
    parent = serializers.SerializerMethodField()
    slug = serializers.CharField(read_only=True)
    products = ShortProductSerializer(source="product_set", many=True)

    class Meta:
        model = Category
        # fields = ('current_user','user', 'parent','slug', 'name', 'date_added', 'image', 'views_count')
        fields = ('url','owner', 'parent','slug', 'name', 'date_added', 'image', 'views_count','products')

    # def get_image_url(self, obj):
    #     return obj.image.url

    def get_parent(self, obj):
        if obj.parent:
            return obj.parent.name
        return None

    #    # Use this method for the custom field
    def _owner(self, obj):
        if obj.owner:
            return obj.owner.username
        return None
